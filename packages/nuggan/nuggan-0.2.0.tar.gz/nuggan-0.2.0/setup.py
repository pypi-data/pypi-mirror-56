# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nuggan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nuggan',
    'version': '0.2.0',
    'description': 'A library for creating self-aware ids',
    'long_description': "# Nuggan\n\nA library for creating informed ids. Nuggan ids aim to provide the\nfollowing properties.\n\n- The id knows the type of entity it is identifying.\n- The authenticity of an id can be established just by looking at the id\n  value. That is to say that a `nuggan` user can determine whether an id given\n  to them is one they previously generated.\n- The alphabetical ordering of a list of ids is relatively equivalent to\n  their chronological ordering.\n\n## Usage\n\nUse `nuggan` to generate ids that encode information about the entity being\nidentified.\n\n```python\nimport nuggan\n\nnuggan.create_id('user')\n# user-005dd1c485-7367ea24-e668-4944-9de0-723112eb1089-e8d26af99684\n```\n\nWhen given an id it can be parsed to identify what it applies to.\n\n```python\nmy_id = 'user-005dd1c485-7367ea24-e668-4944-9de0-723112eb1089-e8d26af99684'\nnuggan.parse_id(my_id)\n# {\n#   'prefix': 'user',\n#   'hex_time': '005dd1c485',\n#   'prefixed_id': 'user-005dd1c485-7367ea24-e668-4944-9de0-723112eb1089',\n#   'base_id': '7367ea24-e668-4944-9de0-723112eb1089',\n#   'checksum': 'e8d26af99684'\n# }\n```\n\nIds have checksums associated with them to allow corrupted ids to be\nidentified.\n\n```python\nbad_id = 'user-005dd1c485-44cc2faf-look-this-aint-rightdfd965a-4a6e8fc57d86'\nnuggan.is_valid_id(bad_id)\n# False\n```\n\nA salt can be configured to give some amount of confidence that a given\nid originated from a specific source.\n\n```python\nmaker = nuggan.IdMaker(salt='an-arbitrary-salt-value')\nsalted_id = maker.create_id('user')\n# user-005dd1c5b4-e4d94f47-cae0-4f16-a0d8-a953c9bd7209-d93cd221c394\nnormal_id = nuggan.create_id('user')\n# user-005dd1c5d8-fd007e41-833f-4c00-8aa9-a26314142845-895de953856b\n\nmaker.is_valid_id(salted_id)\n# True\nmaker.is_valid_id(normal_id)\n# False\n```\n",
    'author': 'Kevin Schiroo',
    'author_email': 'kjschiroo@gmail.com',
    'url': 'https://github.com/kjschiroo/nuggan',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
