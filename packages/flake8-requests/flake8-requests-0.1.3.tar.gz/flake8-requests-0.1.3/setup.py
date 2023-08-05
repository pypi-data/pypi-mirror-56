# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_requests']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.7.9,<4.0.0', 'pytest>=5.3.0,<6.0.0']

entry_points = \
{'flake8.extension': ['r2c-requests-no-auth-over-http = '
                      'flake8_requests.no_auth_over_http:NoAuthOverHttp',
                      'r2c-requests-use-scheme = '
                      'flake8_requests.use_scheme:UseScheme',
                      'r2c-requests-use-timeout = '
                      'flake8_requests.use_timeout:UseTimeout']}

setup_kwargs = {
    'name': 'flake8-requests',
    'version': '0.1.3',
    'description': 'r2c checks for requests',
    'long_description': '\n# flake8-requests\n\nflake8-requests is a plugin for flake8 with checks specifically for the [request](https://pypi.org/project/requests/) framework.\n\n## Installation\n\n```\npip install flake8-requests\n```\n\nValidate the install using `--version`. flake8-requests adds two plugins, but this will be consolidated in a very near-future version. :)\n\n```\n> flake8 --version\n3.7.9 (mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1, flake8-requests)\n```\n\n## List of warnings\n- R2C701="flake8_requests.no_auth_over_http:NoAuthOverHttp"\n- R2C702="flake8_requests.use_timeout:UseTimeout"\n- R2C703="flake8_requests.use_scheme:UseScheme"\n',
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
