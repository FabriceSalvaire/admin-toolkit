####################################################################################################

from collections import namedtuple

####################################################################################################

_NAMEDTUPLE_CACHE = {}

def to_namedtuple(cls: str, data: dict):
    # Fixme: check fields
    if cls not in _NAMEDTUPLE_CACHE:
        fields = sorted(data.keys())
        _NAMEDTUPLE_CACHE[cls] = namedtuple(cls, fields)
    return _NAMEDTUPLE_CACHE[cls](**data)
