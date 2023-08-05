"""Module for creating ids"""
import hashlib
import uuid


def create_id(
        prefix: str,
        salt: str = None,
) -> str:
    """
    Create an id string.

    :param prefix:
        The prefix with which to prefix the generated id. This should be used
        to identify what the id is being applied to.
    :param salt:
        A salt value to use when generating the checksum. Providing a salt
        will make it so the checksum is not strickly determined by the id,
        making forged ids non-trivial.
    """
    if '-' in prefix:
        raise ValueError('prefix cannot contain the "-" character.')
    identifier = prefix + '-' + str(uuid.uuid4())
    return _append_hash(identifier, salt=salt)


def is_valid_id(id_value: str, salt: str = None) -> bool:
    """
    Validate that the given id has a valid checksum.

    :param id_value:
        The id value being tested.
    :param salt:
        A random string value that was used as the `salt` when calling
        `create_id` to generate the id.
    :return:
        True if the id is valid, False if it is either not a valid id or has
        an invalid checksum.
    """
    try:
        parsed = parse_id(id_value)
    except ValueError:
        # It isn't even a valid nuggan id.
        return False
    expected = _append_hash(parsed['prefixed_id'], salt=salt)
    return id_value == expected


def _append_hash(identifier: str, salt: str = None) -> str:
    """Append the hash of the identifier to the identifier."""
    salt = salt or ''
    salted = salt + identifier
    hashed = hashlib.sha1(salted.encode()).hexdigest()
    return identifier + '-' + hashed[:12]


def parse_id(id_value: str) -> dict:
    """
    Parse the id_value into its component parts.

    :param id_value:
        The id value to parse.
    :return:
        A dictionary containing the parts of the id including the prefix,
        uuid, and checksum.
    """
    if len(id_value.split('-')) != 7:
        template = '"{value}" is not a nuggan id.'
        raise ValueError(template.format(value=id_value))
    prefix, remaining = id_value.split('-', maxsplit=1)
    base_id, checksum = remaining.rsplit('-', maxsplit=1)
    prefixed_id, _ = id_value.rsplit('-', maxsplit=1)
    return {
        'prefix': prefix,
        'prefixed_id': prefixed_id,
        'base_id': base_id,
        'checksum': checksum
    }


class IdMaker:
    """Class for generating and validating ids."""

    def __init__(self, salt: str = None):
        self._salt = salt

    def create_id(self, prefix: str) -> str:
        """
        Create an id with the given prefix.

        :param prefix:
            The prefix to prepend to the id.
        :return:
            An id string with the given prefix.
        """
        return create_id(prefix, salt=self._salt)

    def is_valid_id(self, id_value: str) -> bool:
        """
        Validate that the given id is valid.

        :param id_value:
            The id value being tested.
        :param salt:
            A random string value that was used as the `salt` when calling
            `create_id` to generate the id.
        :return:
            True if the id is valid, False if it is either not a valid id
            or has an invalid checksum.
        """
        return is_valid_id(id_value, salt=self._salt)
