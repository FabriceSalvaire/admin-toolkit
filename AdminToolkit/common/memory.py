
####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['compute_memory_size']

####################################################################################################

from collections import deque
from itertools import chain
from reprlib import repr
from sys import getsizeof, stderr

####################################################################################################

def compute_memory_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    def dict_handler(d):
        return chain.from_iterable(d.items())

    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)   # user handlers take precedence
    seen = set()                    # track which object id's have already been seen
    default_size = getsizeof(0)     # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:   # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for type_, handler in all_handlers.items():
            if isinstance(o, type_):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

####################################################################################################


if __name__ == '__main__':
    d = dict(a=1, b=2, c=3, d=[4, 5, 6, 7], e='a string of chars')
    print(compute_memory_size(d, verbose=True))
