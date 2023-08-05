# Nuggan

A library for creating self-aware ids.

## Usage

Use `nuggan` to generate ids that encode information about the entity being
identified.

```python
import nuggan

nuggan.create_id('user')
# user-44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a-4a6e8fc57d86
```

When given an id it can be parsed to identify what it applies to.

```python
my_id = 'user-44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a-4a6e8fc57d86'
nuggan.parse_id(my_id)
# {
#     'prefix': 'user',
#     'prefixed_id': 'user-44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a',
#     'base_id': '44cc2faf-b1a4-47ad-a1fe-4bc81dfd965a',
#     'checksum': '4a6e8fc57d86'
# }
```

Ids have checksums associated with them to allow corrupted ids to be
identified.

```python
corrupted_id = 'user-44cc2faf-look-this-aint-rightdfd965a-4a6e8fc57d86'
nuggan.is_valid_id(corrupted_id)
# False
```

A salt can be configured to give some amount of confidence that a given
id originated from a specific source.

```python
maker = nuggan.IdMaker(salt='an-arbitrary-salt-value')
salted_id = maker.create_id('user')
# user-99a528df-ff28-435d-8fc6-1c1f51aaa7c2-5b70075ae688
normal_id = nuggan.create_id('user')
# user-ffe386b7-689c-4ab7-95b4-304fa83a64a0-35d605d62ffa

maker.is_valid_id(salted_id)
# True
maker.is_valid_id(normal_id)
# False
```
