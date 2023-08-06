# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['escarpolette',
 'escarpolette.admin',
 'escarpolette.api',
 'escarpolette.models',
 'escarpolette.rules']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'flask-cors>=3.0,<4.0',
 'flask-login>=0.4.1,<0.5.0',
 'flask-migrate>=2.5,<3.0',
 'flask-restplus>=0.12.1,<0.13.0',
 'flask-sqlalchemy>=2.3,<3.0',
 'flask>=1.0,<2.0',
 'gevent>=1.4,<2.0',
 'sqlalchemy>=1.2,<2.0',
 'youtube-dl>=2019.1,<2020.0']

entry_points = \
{'console_scripts': ['escarpolette = escarpolette:__main__']}

setup_kwargs = {
    'name': 'escarpolette',
    'version': '0.2.0',
    'description': 'Manage your musical playlist with your friends without starting a war.',
    'long_description': '# Escarpolette\n\nThis project provides a server and clients to manage your music playlist when you are hosting a party.\n\nIt supports many sites, thanks to the awesome project [youtube-dl](https://rg3.github.io/youtube-dl/).\n\n## Features\n\nServer:\n* add items (and play them!)\n* get playlist\'s itmes\n* runs on Android! (see [instructions](#Android))\n\nWeb client:\n* there is currently no web client :(\n\n## Dependencies\n\n* Python 3.6\n* the dependencies manager [Poetry](https://poetry.eustace.io/)\n* the player [mpv](https://mpv.io)\n\nThey should be available for most of the plateforms.\n\n\n## Installation\n\n```Shell\npip install escarpolette\n# generate a random secret key\necho "SECRET_KEY = \'$(cat /dev/urandom | tr -dc \'a-zA-Z0-9\' | fold -w 32 | head -n 1)\'" > config.cfg\n```\n\n### Android\n\nYou will need [Termux](https://termux.com/).\nThen inside Termux you can install it with:\n\n```Shell\n# dependencies\npkg install python python-dev clang\n# escarpolette\npip install escarpolette\n```\n\nNote that while the project can run without wake-lock, acquiring it improve the performance (with a battery trade off).\n\n## Usage\n\n```Shell\nescarpolette --config config.cfg\n```\n\n## Todo\n\n* server\n    * empty the playlist on startup\n    * bonjour / mDNS\n    * votes\n    * prevent adding youtube / soundcloud playlists\n    * restrictions by users\n    * configuration of those restrictions by an admin\n* web client\n    * show playing status\n    * votes\n    * configure restrictions:\n        * max video added per user\n        * max video length\n    * admin access:\n        * configure restrictions\n        * no restrictions for him\n        * force video order\n\nDon\'t count on it:\n* android client\n* iOS client\n',
    'author': 'Alexandre Morignot',
    'author_email': 'erdnaxeli@cervoi.se',
    'url': 'https://github.com/erdnaxeli/escarpolette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
