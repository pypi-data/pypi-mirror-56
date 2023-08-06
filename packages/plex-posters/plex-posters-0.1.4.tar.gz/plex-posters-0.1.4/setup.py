# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['plex_posters',
 'plex_posters.__dev',
 'plex_posters.config',
 'plex_posters.library']

package_data = \
{'': ['*'], 'plex_posters': ['test/*']}

install_requires = \
['praw>=6.4,<7.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'plex-posters',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'dtomlinson',
    'author_email': 'dtomlinson@panaetius.co.uk',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
