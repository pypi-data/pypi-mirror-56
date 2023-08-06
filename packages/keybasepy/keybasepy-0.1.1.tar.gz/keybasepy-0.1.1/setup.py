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
    'version': '0.1.1',
    'description': 'A bot library for keybase',
    'long_description': '# keybase.py\n\nThis is a keybase wrapper for Python 3.7+\n\n## Install\n\n```sh\npython setup.py install\n```\n\n## Todo\n\n* [ ] Add documentation.\n* [ ] Release on PyPi\n* [ ] Create a more comprehensive README\n',
    'author': 'dnorhoj',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
