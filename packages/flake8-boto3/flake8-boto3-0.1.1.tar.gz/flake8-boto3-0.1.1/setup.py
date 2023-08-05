# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_boto3']

package_data = \
{'': ['*']}

install_requires = \
['astunparse>=1.6.2,<2.0.0',
 'boto3>=1.10.21,<2.0.0',
 'flake8>=3.7.9,<4.0.0',
 'pytest>=5.3.0,<6.0.0']

entry_points = \
{'flake8.extension': ['r2c-avoid-hardcoded-access-token = '
                      'flake8_boto3.auth:CheckHardcodedAccessTokens',
                      'r2c-boto3-dont-use-deprecated-api = '
                      'flake8_boto3.deprecated:CheckDeprecatedAPI',
                      'r2c-use-boto3-over-boto = '
                      'flake8_boto3.boto_import:CheckInvalidBotoImport']}

setup_kwargs = {
    'name': 'flake8-boto3',
    'version': '0.1.1',
    'description': 'r2c flake8 check',
    'long_description': '# Flake8 Example\n\n## Setup\n\n    pip install -r requirements.txt\n\n\n## Install\n\n    pip install -e .\n\n## Running\n\n    flake8 --select X1 examples/jared.py\n\n## Testing\n\n    pytest\n',
    'author': 'R2C',
    'author_email': 'hello@returntocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://r2c.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
