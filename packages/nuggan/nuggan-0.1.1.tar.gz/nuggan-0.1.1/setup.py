# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nuggan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nuggan',
    'version': '0.1.1',
    'description': 'A library for creating self-aware ids',
    'long_description': "# Nuggan\n\nA library for creating self-aware ids.\n\n## Usage\n\nUse `nuggan` to generate ids that encode information about the entity being\nidentified.\n\n```python\nimport nuggan\n\nnuggan.create_id('user')\n# user-44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a-4a6e8fc57d86\n```\n\nWhen given an id it can be parsed to identify what it applies to.\n\n```python\nmy_id = 'user-44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a-4a6e8fc57d86'\nnuggan.parse_id(my_id)\n# {\n#     'prefix': 'user',\n#     'prefixed_id': 'user-44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a',\n#     'base_id': '44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a',\n#     'checksum': '4a6e8fc57d86'\n# }\n```\n\nIds have checksums associated with them to allow corrupted ids to be\nidentified.\n\n```python\ncorrupted_id = 'user-44cc2faf-look-this-aint-rightdfd965a-4a6e8fc57d86'\nnuggan.is_valid_id(corrupted_id)\n# False\n```\n\nA salt can be configured to give some amount of confidence that a given\nid originated from a specific source.\n\n```python\nmaker = nuggan.IdMaker(salt='an-arbitrary-salt-value')\nsalted_id = maker.create_id('user')\n# user-99a528df-ff28-435d-8fc6-1c1f51aaa7c2-5b70075ae688\nnormal_id = nuggan.create_id('user')\n# user-ffe386b7-689c-4ab7-95b4-304fa83a64a0-35d605d62ffa\n\nmaker.is_valid_id(salted_id)\n# True\nmaker.is_valid_id(normal_id)\n# False\n```\n",
    'author': 'Kevin Schiroo',
    'author_email': 'kjschiroo@gmail.com',
    'url': 'https://github.com/kjschiroo/nuggan',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
