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
['flask-cors>=3.0,<4.0',
 'flask-login>=0.4.1,<0.5.0',
 'flask-migrate>=2.5,<3.0',
 'flask-restplus>=0.12.1,<0.13.0',
 'flask-sqlalchemy>=2.3,<3.0',
 'flask>=1.0,<2.0',
 'sqlalchemy>=1.2,<2.0',
 'youtube-dl>=2019.1,<2020.0']

setup_kwargs = {
    'name': 'escarpolette',
    'version': '0.1.1',
    'description': 'Manage your musical playlist with your friends without starting a war.',
    'long_description': "# Escarpolette\n\nThis project provides a server and clients to manage your music playlist when you are hosting a party.\n\nIt supports many sites, thanks to the awesome project [youtube-dl](https://rg3.github.io/youtube-dl/).\n\n## Features\n\nServer:\n* add items (and play them!)\n* get playlist's itmes\n* runs on Android! (see [instructions](#Android))\n\nWeb client:\n* there is currently no web client :(\n\n## Dependencies\n\n* Python 3.6\n* the dependencies manager [Poetry](https://poetry.eustace.io/)\n* the player [mpv](https://mpv.io)\n\nThey should be available for most of the plateforms.\n\n\n## Run it\n\n### Linux\n\nClone the repository, then go the folder and type:\n\n```Shell\nmake init\nmake db-upgrade\nmake run\n```\n\nYou can now open [localhost:5000](http://localhost:5000).\nJust add a new item to get the music playing!\n\n### Android\n\nYou will need [Termux](https://termux.com/).\nThen inside Termux you can install the dependencies with:\n\n```Shell\npkg install python python-dev clang git make\npip install poetry\n```\n\nThen follow the Linux instructions.\nNote that while the project can run without wake-lock, acquiring it improve the performance (with a battery trade off).\n\n## Todo\n\n* server\n    * empty the playlist on startup\n    * bonjour / mDNS\n    * votes\n    * prevent adding youtube / soundcloud playlists\n    * restrictions by users\n    * configuration of those restrictions by an admin\n* web client\n    * show playing status\n    * votes\n    * configure restrictions:\n        * max video added per user\n        * max video length\n    * admin access:\n        * configure restrictions\n        * no restrictions for him\n        * force video order\n\nDon't count on it:\n* android client\n* iOS client\n",
    'author': 'Alexandre Morignot',
    'author_email': 'erdnaxeli@cervoi.se',
    'url': 'https://github.com/erdnaxeli/escarpolette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
