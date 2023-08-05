# Nuggan

A library for creating informed ids. Nuggan ids aim to provide the
following properties.

- The id knows the type of entity it is identifying.
- The authenticity of an id can be established just by looking at the id
  value. That is to say that a `nuggan` user can determine whether an id given
  to them is one they previously generated.
- The alphabetical ordering of a list of ids is relatively equivalent to
  their chronological ordering.

## Usage

Use `nuggan` to generate ids that encode information about the entity being
identified.

```python
import nuggan

nuggan.create_id('user')
# user-005dd1c485-7367ea24-e668-4944-9de0-723112eb1089-e8d26af99684
```

When given an id it can be parsed to identify what it applies to.

```python
my_id = 'user-005dd1c485-7367ea24-e668-4944-9de0-723112eb1089-e8d26af99684'
nuggan.parse_id(my_id)
# {
#   'prefix': 'user',
#   'hex_time': '005dd1c485',
#   'prefixed_id': 'user-005dd1c485-7367ea24-e668-4944-9de0-723112eb1089',
#   'base_id': '7367ea24-e668-4944-9de0-723112eb1089',
#   'checksum': 'e8d26af99684'
# }
```

Ids have checksums associated with them to allow corrupted ids to be
identified.

```python
bad_id = 'user-005dd1c485-44cc2faf-look-this-aint-rightdfd965a-4a6e8fc57d86'
nuggan.is_valid_id(bad_id)
# False
```

A salt can be configured to give some amount of confidence that a given
id originated from a specific source.

```python
maker = nuggan.IdMaker(salt='an-arbitrary-salt-value')
salted_id = maker.create_id('user')
# user-005dd1c5b4-e4d94f47-cae0-4f16-a0d8-a953c9bd7209-d93cd221c394
normal_id = nuggan.create_id('user')
# user-005dd1c5d8-fd007e41-833f-4c00-8aa9-a26314142845-895de953856b

maker.is_valid_id(salted_id)
# True
maker.is_valid_id(normal_id)
# False
```
