####################################################################################################

__all__ = ['to_namedtuple']

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

####################################################################################################

def namedtuple_factory(cls_name: str, fields: [str]):
    return namedtuple(
        cls_name,
        fields,
        defaults=[None]*len(fields),
    )
