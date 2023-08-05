# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['peperoncino', 'peperoncino.processings']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'pandas>=0.25.3,<0.26.0']

setup_kwargs = {
    'name': 'peperoncino',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Junki Ishikawa',
    'author_email': '69guitar1015@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.７,<4.0',
}


setup(**setup_kwargs)
