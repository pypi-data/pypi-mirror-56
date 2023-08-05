from setuptools import setup, find_packages, os
import sys

APP = ['oktaauth/okta_awscli.py']
DATA_FILES = ['oktaauth/aws_auth.py','oktaauth/version.py' ,'oktaauth/okta_auth_config.py', 'oktaauth/okta_auth.py', 'oktaauth/__init__.py']
OPTIONS = {'argv_emulation': True,
    'iconfile': 'icon.icns',
    'packages': ['requests',
        'click',
        'bs4',
        'boto3',
        'ConfigParser',
        'keyring',
        'tzlocal',
        ]
    }

here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'oktaauth/version.py')).read())

setup(
    name='okta-awsauth',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'boto3', 'setuptools'],
    version=__version__,
    description='Provides a wrapper for Okta authentication to awscli',
    packages=find_packages(),
    license='Apache License 2.0',
    author='Franco Papalardo',
    author_email='franco.papalardo@ownzones.com',
    url='https://github.com/OwnZones/okta-awscli',
    entry_points={
        'console_scripts': [
            'okta-awscli=oktaauth.okta_awscli:main',
        ],
    },
    install_requires=[
        'requests',
        'click',
        'bs4',
        'boto3',
        'ConfigParser',
        'keyring',
        'tzlocal',
        ],
    extras_require={
        'U2F': ['python-u2flib-host']
    },
    python_requires='>=3.6'
)
