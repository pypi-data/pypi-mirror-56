# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aio_pika_rpc']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.3', 'ddtrace>=0.30', 'msgpack>=0.6']

setup_kwargs = {
    'name': 'aio-pika-rpc',
    'version': '1.2.0',
    'description': 'aio-pika RPC',
    'long_description': '# aio-pika-msgpack-rpc\n\naio-pika msgpack RPC\n',
    'author': 'm.shlyamov',
    'author_email': 'm.shlyamov@yandex.com',
    'url': 'https://github.com/SandLabs/aio-pika-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
