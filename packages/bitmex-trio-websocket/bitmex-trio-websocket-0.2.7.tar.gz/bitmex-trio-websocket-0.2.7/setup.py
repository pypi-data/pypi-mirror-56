# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bitmex_trio_websocket']

package_data = \
{'': ['*']}

install_requires = \
['trio-websocket>=0.8.0,<0.9.0', 'ujson>=1.35,<2.0']

setup_kwargs = {
    'name': 'bitmex-trio-websocket',
    'version': '0.2.7',
    'description': 'Websocket implementation for BitMEX cryptocurrency derivatives exchange.',
    'long_description': None,
    'author': 'Anders Ellenshøj Andersen',
    'author_email': 'andersa@ellenshoej.dk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
