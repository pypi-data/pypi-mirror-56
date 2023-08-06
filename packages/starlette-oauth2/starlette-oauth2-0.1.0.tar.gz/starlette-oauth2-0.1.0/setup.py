import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='starlette-oauth2',
    version='0.1.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['starlette_oauth2'],
    install_requires=[
        'starlette>=0.13.0,<1',
        'authlib>=0.13,<0.14',
        'requests>=2,<3',
        'itsdangerous>=1.1,<2',
    ]
)
