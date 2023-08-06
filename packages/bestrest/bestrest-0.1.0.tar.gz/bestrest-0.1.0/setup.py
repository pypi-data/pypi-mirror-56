# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bestrest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bestrest',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Giovanni Cardamone',
    'author_email': 'giovanni.cardamone@becar.it',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
