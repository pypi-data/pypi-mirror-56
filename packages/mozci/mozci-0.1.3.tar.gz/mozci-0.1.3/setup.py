# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mozci']

package_data = \
{'': ['*'], 'mozci': ['queries/*']}

install_requires = \
['adr>=0.16.5,<0.17.0']

setup_kwargs = {
    'name': 'mozci',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@mozilla.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
