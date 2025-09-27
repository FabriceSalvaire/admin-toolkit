####################################################################################################

__all__ = ['bool_from_json', 'fix_dict_key']

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
