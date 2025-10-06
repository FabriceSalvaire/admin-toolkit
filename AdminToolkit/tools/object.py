####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = [
    'split_line',
    # 'bool_from_json',
    'fix_dict_key',
    'to_namedtuple', 'namedtuple_factory',
]

####################################################################################################

from collections import namedtuple
from typing import Any
from pprint import pprint
import json
import uuid

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

# def bool_from_json(value: str) -> bool:
#     return value == 'true'

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

def load_json(stream: str, cls_map: dict = None) -> dict:
    def object_hook(d):
        # print('---')
        # print('object_hook')
        # pprint(d)
        # print('---')
        fix_dict_key(d)
        for key, value in d.items():
            if not value:
                continue
            match value:
                case 'true':
                    d[key] = True
                case 'false':
                    d[key] = False
                case str():
                    if '.' in value:
                        try:
                            d[key] = float(value)
                        except ValueError:
                            pass
                    elif value[0].isnumeric():
                        try:
                            d[key] = int(value)
                        except ValueError:
                            pass
        for key in d.keys():
            if cls_map and key in cls_map:
                _ = d[key]
                d[key] = cls_map[key](_)
        return d

    data = json.loads(
        stream,
        # cls=None,
        object_hook=object_hook,
        parse_float=None,  # float(num_str)
        # parse_int=None,   # int(num_str)
        # parse_constant=None,
        # object_pairs_hook=object_hook,
    )
    return data

####################################################################################################

_NAMEDTUPLE_CACHE = {}

def to_namedtuple(cls: str, data: dict):
    # Fixme: check fields
    if cls not in _NAMEDTUPLE_CACHE:
        fields = sorted(data.keys())
        # print(f"new cls {cls} {fields}")
        _NAMEDTUPLE_CACHE[cls] = namedtuple(cls, fields)
    # else:
    #     print(f"cached cls {cls}")
    return _NAMEDTUPLE_CACHE[cls](**data)

####################################################################################################

def namedtuple_factory(cls_name: str, fields: [str]):
    return namedtuple(
        cls_name,
        fields,
        defaults=[None]*len(fields),
    )

####################################################################################################

def objectify(name: str, data: dict) -> Any:
    suffix = str(uuid.uuid1()).replace('-', '')[:10]
    name = f'{name}_{suffix}'
    obj = to_namedtuple(name, data)
    return obj

####################################################################################################


if __name__ == '__main__':

    stream = '''
{
    "f1": "abc",
    "f2": "123",
    "f3": "1.23",
    "f4": 123,
    "f5": 1.23,
    "f6": "true",
    "f7": "false",
    "d1": {
        "a": [1, 2, 3],
        "b": "b"
    }
}
'''
    pprint(load_json(stream))
