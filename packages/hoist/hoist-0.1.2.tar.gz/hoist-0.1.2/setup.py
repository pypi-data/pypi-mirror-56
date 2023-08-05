# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hoist']

package_data = \
{'': ['*'],
 'hoist': ['web_files/*', 'web_files/static/css/*', 'web_files/static/js/*']}

install_requires = \
['aiohttp>=3.5,<4.0',
 'jinja2>=2.10,<3.0',
 'toml>=0.10.0,<0.11.0',
 'websockets>=7.0,<8.0']

entry_points = \
{'console_scripts': ['hoist = hoist:main']}

setup_kwargs = {
    'name': 'hoist',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Shady Rafehi',
    'author_email': 'shadyrafehi@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
