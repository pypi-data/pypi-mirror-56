# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keybasepy']

package_data = \
{'': ['*']}

install_requires = \
['pykeybasebot>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'keybasepy',
    'version': '0.1.0',
    'description': 'A bot library for keybase',
    'long_description': None,
    'author': 'dnorhoj',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
