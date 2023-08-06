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
    'version': '0.2.8',
    'description': 'Websocket implementation for BitMEX cryptocurrency derivatives exchange.',
    'long_description': "# BitMEX Trio-Websocket\n\n\n[![PyPI](https://img.shields.io/pypi/v/bitmex_trio_websocket.svg)](https://pypi.python.org/pypi/bitmex-trio-websocket)\n[![Build Status](https://img.shields.io/travis/com/andersea/bitmex-trio-websocket.svg)](https://travis-ci.com/andersea/bitmex-trio-websocket)\n[![Read the Docs](https://readthedocs.org/projects/bitmex-trio-websocket/badge/?version=latest)](https://bitmex-trio-websocket.readthedocs.io/en/latest/?badge=latest)\n\nWebsocket implementation for BitMEX cryptocurrency derivatives exchange.\n\n* Free software: MIT license\n* Documentation: https://bitmex-trio-websocket.readthedocs.io.\n\n## Features\n\n* Connects to BitMEX websockets for a given symbol or lists of symbols.\n* Supports authenticated connections using api keys.\n* Fully async using async generators. No callbacks or event emitters.\n* Based on trio and trio-websocket.\n\n## Installation\n\nThis library requires Python 3.7 or greater. It could probably be made to run with Python 3.6, since this\nis the minimal version where async generators are supported. To install from PyPI:\n\n    pip install bitmex-trio-websocket\n\n## Client example\n\n    import trio\n\n    from bitmex_trio_websocket import BitMEXWebsocket\n\n    async def main():\n        bws = BitMEXWebsocket('mainnet', 'XBTUSD')\n        async for message in bws.start():\n            print(message)\n\n    trio.run(main)\n\nThis will print a sequence of tuples of the form `(item, symbol|None, table, action)`, where -\n\n`item` is the full object resulting from inserting or merging the changes to an item.\n \n`symbol` is the symbol that was changed or `None` if the table isn't a symbol table.\n\n`table` is the table name.\n\n`action` is the action that was taken.\n\nNote, that delete actions are simply applied and consumed, with no output sent.\n\n## API\n\n![bitmex__trio__websocket.BitMEXWebsocket](https://img.shields.io/badge/class-bitmex__trio__websocket.BitMEXWebsocket-blue?style=flat-square)\n\n![constructor](https://img.shields.io/badge/constructor-BitMEXWebsocket(endpoint%2C%20symbol%2C%20api__key%2C%20api__secret)-blue)\n\nCreates a new websocket object.\n\n**`endpoint`** str\n\nNetwork to connect to. Options: 'mainnet', 'testnet'.\n\n**`symbol`** Optional\\[Union\\[str, Iterable\\[str\\]\\]\\]\n\nSymbols to subscribe to. Each symbol is subscribed to the following channels: ['instrument', 'quote', 'trade', 'tradeBin1m']. If not provided, no instrument channels are subscribed for this connection. This may be useful if you only want to connect to authenticated channels.\n\n**`api_key`** Optional\\[str\\]\n\nApi key for authenticated connections. If a valid api key and secret is supplied, the following channels are subscribed: ['margin', 'position', 'order', 'execution'].\n\n**`api_secret`** Optional\\[str\\]\n\nApi secret for authenticated connections.\n\n![await start](https://img.shields.io/badge/await-start()-green)\n\nReturns an async generator object that yields messages from the websocket.\n\n![storage](https://img.shields.io/badge/attribute-storage-teal)\n\nThis attribute contains the storage object for the websocket. The storage object has two properties `data` and `keys`. `data` contains the table state for each channel as a dictionary with the table name as key. The tables themselves are flat lists. `keys` contains a list of keys by which to look up values in each table. There is a helper function `findItemByKeys` in the storage unit, which assists in finding particular items in each table. Tables are searched sequentially until a match is found, with is somewhat inefficient. However since there is never a lot of records in each table (at most 200), this is reasonably fast in practice and not a bottleneck.\n\n![ws](https://img.shields.io/badge/attribute-ws-teal)\n\nWhen connected, contains the underlying trio-websocket object. Can be used to manage the connection.\n\nSee - https://trio-websocket.readthedocs.io/en/stable/api.html#connections\n\n## Credits\n\nThanks to the [Trio](https://github.com/python-trio/trio) and [Trio-websocket](https://github.com/HyperionGray/trio-websocket) libraries for their awesome work.\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.\n",
    'author': 'Anders Ellenshøj Andersen',
    'author_email': 'andersa@ellenshoej.dk',
    'url': 'https://github.com/andersea/bitmex-trio-websocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
