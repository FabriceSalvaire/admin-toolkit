####################################################################################################

__all__ = ['Locate']

####################################################################################################

from typing import Iterator, Self

from . import object
from .object import Path

####################################################################################################

class Filter:

    ##############################################

    def __init__(self) -> None:
        pass

    ##############################################

    def __mul__(self, filter: 'Filter') -> Self:
        return filter

####################################################################################################

class SourceFilter:

    ##############################################

    def __mul__(self, filter: 'Filter') -> Self:
        return Pipe(self) * filter

####################################################################################################

class Pipe:

    ##############################################

    def __init__(self, source: SourceFilter) -> None:
        # self._source = source
        self._filters = [source]

    ##############################################

    def __mul__(self, filter: 'Filter') -> Self:
        self._filters.append(filter)
        return self

####################################################################################################

class Locate(SourceFilter):

    ##############################################

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._args = args
        self._kwargs = kwargs

    ##############################################

    def run(self) -> Iterator[Path]:
        from .interface.locate import locate
        for _ in locate(*self._args, **self._kwargs):
            yield Path.make(_)

#####################################################################################################

class Directory(Filter):

    ##############################################

    def run(self, input: Iterator[Path]) -> Iterator[Path]:
        for _ in input:
            if isinstance(_, object.Directory):
                yield _

#####################################################################################################

class ByName(Filter):

    ##############################################

    def __init__(self, name: str) -> None:
        self._name = str(name)

    ##############################################

    def run(self, input: Iterator[Path]) -> Iterator[Path]:
        name = self._name
        for _ in input:
            if _.name == name:
                c = _.parts.count(name)
                if c == 1:
                    yield _

####################################################################################################

# def locate_node_modules() -> Iterator[str]:
#     NODE_MODULES = 'node_modules'
#     for _ in locate(NODE_MODULES):
#         _ = Path(_)
#         if _.name == NODE_MODULES:
#             c = _.parts.count(NODE_MODULES)
#             parent = str(_.parent)
#             if c == 1 and NODE_MODULES not in parent and '.pnpm' not in parent:
#                 print(_)
