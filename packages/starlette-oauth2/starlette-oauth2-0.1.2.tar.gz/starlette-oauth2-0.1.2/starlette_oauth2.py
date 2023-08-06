import typing
import logging

from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send
from authlib.integrations._client import UserInfoMixin, RemoteApp as _RemoteApp, errors
from authlib.integrations.requests_client import OAuth2Session


logger = logging.getLogger(__name__)


class RemoteApp(_RemoteApp, UserInfoMixin):
    """A RemoteApp for Starlette framework."""
    def __init__(self, **kwargs) -> None:
        super().__init__(oauth2_client_cls=OAuth2Session, **kwargs)

    def _generate_access_token_params(self, request):
        if self.request_token_url:
            return request.scope
        return {
            'code': request.query_params.get('code'),
            'state': request.query_params.get('state'),
        }

    def authorize_redirect(self, request, redirect_uri=None, **kwargs):
        rv = self.create_authorization_url(redirect_uri, **kwargs)
        self.save_authorize_data(request, redirect_uri=redirect_uri, **rv)
        return RedirectResponse(rv['url'])

    def authorize_access_token(self, request, **kwargs):
        params = self.retrieve_access_token_params(request)
        params.update(kwargs)
        return self.fetch_access_token(**params)

    def parse_id_token(self, request, token, claims_options=None):
        """Return an instance of UserInfo from token's ``id_token``."""
        if 'id_token' not in token:
            return None

        return self._parse_id_token(request, token, claims_options)


class AuthenticateMiddleware:
    REDIRECT_PATH = '/authorized'
    PROVIDERS = {
        'microsoft': {
            'name': 'microsoft',
            'server_metadata_url': 'https://login.microsoftonline.com/{}/v2.0/.well-known/openid-configuration',
            'is_member_url': 'https://graph.microsoft.com/v1.0/me/checkMemberGroups'
        },
        'google': {
            'name': 'google',
            'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration',
        },
    }
    PROVIDER = PROVIDERS['microsoft']

    def __init__(self, app: ASGIApp, db, tenant_id: str, client_id: str, client_secret: str, roles, force_https_redirect=True) -> None:
        self.app = app
        self.db = db
        self._roles = roles
        self._force_https_redirect = force_https_redirect

        self._client = RemoteApp(
            name=self.PROVIDER['name'],
            client_id=str(client_id),
            client_secret=str(client_secret),
            server_metadata_url=self.PROVIDER['server_metadata_url'].format(tenant_id),
            client_kwargs={'scope': 'openid email profile'},
        )

    def path_to_roles(self, path: str) -> typing.Tuple[typing.List[str], str]:
        """
        Overwrite to provide a role-based model based on the path. By default, all paths are available to all authenticated
        users.

        This must return a tuple with a list of roles and `'all'` or `'any'`, e.g. `(['user', 'guest'], 'any')`.
        """
        return [], 'all'

    def _redirect_uri(self, request: Request):
        """
        The URI of the redirect path. This should be registered on whatever provider is declared.
        """
        port = request.url.port
        if port is None:
            port = ''
        else:
            port = ':' + port
        scheme = request.url.scheme
        if scheme == 'http' and self._force_https_redirect:
            scheme = 'https'
        return f"{scheme}://{request.url.hostname}{port}{self.REDIRECT_PATH}"

    def _is_authorized(self, user, token: str, roles: typing.List[str], how: str = 'all'):
        """
        Returns whether the currently authenticated user is authorized based on a set of roles.
        It checks whether it belongs to (all/any, the ``how``) of the groups associated with the roles.
        """
        # if no roles are requested, the user is authorized.
        if not roles:
            return True

        assert how in {'all', 'any'}
        groups = [self._roles[role] for role in roles]

        response = self._client.request(
            'POST', self.PROVIDER['is_member_url'], token=token, json={'groupIds': groups})

        if response.ok:
            data = response.json()
        else:
            # can't tell if the user has access not not => it does not
            return False

        mask = (group in data['value'] for group in groups)

        if how == 'all':
            return all(mask)
        else:
            return any(mask)

    async def _authenticate(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope)

        logger.info(f'Authenticating a user arriving at "{request.url.path}"')

        # /authorized is our redirect_uri and thus the only one that is public
        if request.url.path != self.REDIRECT_PATH:
            # any un-authenticated request is redirected to the tenant
            redirect_uri = self._redirect_uri(request)
            response = self._client.authorize_redirect(request, redirect_uri)
            await response(scope, receive, send)
        else:
            logger.info(f'Fetching id token...')
            # try to construct a user from the access token
            try:
                token = self._client.authorize_access_token(request)
                user = self._client.parse_id_token(request, token)
                assert user is not None
            except:
                # impossible to build a user => invalidate the whole thing and redirect to home (which triggers a new auth)
                response = RedirectResponse(url='/')
                await response(scope, receive, send)
                return

            # we have a user => store it as a signed cookie
            request.session['user'] = dict(user)

            # and the associated token in the database
            logger.info(f'Storing token from user "{user["email"]}"...')
            self.db.put(user['email'], dict(token))

            # finally, redirect to home
            response = RedirectResponse(url='/')
            await response(scope, receive, send)

    def _authorize(self, user, token: str, scope: Scope, receive: Receive, send: Send):
        request = Request(scope)

        roles, how = self.path_to_roles(request.url.path)

        return self._is_authorized(user, token, roles, how)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope)
        user = request.session.get('user')

        # no user => start authentication (it redirects)
        if user is None:
            await self._authenticate(scope, receive, send)
            return

        # fetch the token from the database associated with the user
        token = self.db.get(user['email'])

        if token is None:
            # this should never happen, but to be on the safe side, let's redirect.
            await self._authenticate(scope, receive, send)
            return
        logger.info(f'User "{user["email"]}" is authenticated.')

        # check for authorization. Currently we accept all users. This just checks that the token is still valid.
        try:
            is_authorized = self._authorize(user, token, scope, receive, send)
        except errors.InvalidTokenError:
            # invalidate session and redirect.
            del request.session['user']
            self.db.delete(user['email'])

            redirect_uri = self._redirect_uri(request)
            response = self._client.authorize_redirect(request, redirect_uri)
            await response(scope, receive, send)
            return

        if not is_authorized:
            logger.warning(f'User "{user["email"]}" is un-authorized to request "{request.url.path}"')
            response = JSONResponse({'message': 'You are un-authorized to make this request.'}, status_code=401)
            await response(scope, receive, send)
            return
        else:
            logger.info(f'User "{user["email"]}" is authorized to request "{request.url.path}"')

        await self.app(scope, receive, send)
