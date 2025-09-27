####################################################################################################

__all__ = []

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
