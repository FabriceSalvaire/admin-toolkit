####################################################################################################

__all__ = [
    'split_line',
    'to_namedtuple', 'namedtuple_factory',
    'bool_from_json', 'fix_dict_key',
]

####################################################################################################

from collections import namedtuple

####################################################################################################

def split_line(line: str, filters: list, skip: list = ()) -> list:
    filter_map = {}
    for slice_, filter in filters:
        match slice_:
            case int():
                filter_map[slice_] = filter
            case tuple():
                for i in slice_:
                    filter_map[i] = filter
            case list():
                inf, sup = slice_
                for i in range(inf, sup + 1):
                    filter_map[i] = filter
    output = []
    for i, value in enumerate(line.split()):
        if i in skip:
            continue
        filter = filter_map.get(i, None)
        if filter is not None:
            value = filter(value)
        output.append(value)
    return output

####################################################################################################

def bool_from_json(value: str) -> bool:
    return value == 'true'

####################################################################################################

# def fix_dict_key(d: dict) -> dict:
#     return {key.replace('-', '_'): value for key, value in d.items()}

def fix_dict_key(d: dict) -> dict:
    for key in list(d.keys()):
        if '-' in key or ':' in key or '%' in key:
            new_key = key.replace('-', '_').replace(':', '_').replace('%', 'p')
            d[new_key] = d[key]
            del d[key]
    return d

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
