# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nuggan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nuggan',
    'version': '0.1.0',
    'description': 'A library for creating self-aware ids',
    'long_description': None,
    'author': 'Kevin Schiroo',
    'author_email': 'kjschiroo@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
