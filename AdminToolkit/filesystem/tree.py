####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['Node', 'Directory', 'File', 'Walker']

####################################################################################################

from pathlib import Path
from pprint import pprint
from typing import Iterator
import os

from .walker import WalkerAbc

####################################################################################################

class Node:

    _MAP = {}
    __slots__ = ('_path')

    ##############################################

    def __init__(self, path: Path, root: bool = False) -> None:
        self._path = Path(path)
        if not root:
            try:
                parent = Node._MAP[self.to_hash(self._path.parent)]
            except KeyError as e:
                print(f"KeyError for {self._path.parent}")
                pprint(Node._MAP)
                raise e
            parent.add_child(self)

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    ##############################################

    @property
    def stat(self) -> os.stat_result:
        if self._path.is_symlink() or not self._path.exists():
            return None
        else:
            return self._path.stat()

    @property
    def size(self) -> int:
        _ = self.stat
        if _ is None:
            return 0
        else:
            return _.st_size

    @property
    def disk_size(self) -> int:
        _ = self.stat
        if _ is None:
            return 0
        else:
            return _.st_blocks * 512

    ##############################################

    @classmethod
    def to_hash(cls, path: Path) -> int:
        return hash(str(path))

    ##############################################

    def __hash__(self) -> int:
        return self.to_hash(self._path)

####################################################################################################

class Directory(Node):

    __slots__ = ('_children', '_size_accumulator', '_file_accumulator')

    ##############################################

    def __init__(self, path: Path, root: bool = False) -> None:
        super().__init__(path, root)
        self._children = []
        key = hash(self)
        if key not in Node._MAP:
            Node._MAP[key] = self
        else:
            raise NameError("Duplicate")
        self._size_accumulator = 0   # disk
        self._file_accumulator = 0

    ##############################################

    def __iter__(self) -> Iterator[Node]:
        return iter(self._children)

    def iter_on_directories(self) -> Iterator['Directory']:
        for _ in self._children:
            if isinstance(_, Directory):
                yield _

    def iter_on_files(self) -> Iterator['File']:
        for _ in self._children:
            if isinstance(_, File):
                yield _

    ##############################################

    def __repr__(self) -> str:
        return f'{self._path} -> [' + ', '.join([repr(_) for _ in self._children]) + ']'

    ##############################################

    def add_child(self, child: Node) -> None:
        self._children.append(child)

    ##############################################

    def walk(
        self,
        callback,
        top_down: bool = True,
        depth: int = 0,
        sort_func=None,
        cls_filter=None,
    ) -> None:
        def call(node: Node, depth: int) -> None:
            if not (cls_filter and not isinstance(node, cls_filter)):
                callback(node, depth)

        def by_name(node: Node) -> str:
            return node._path.name

        if top_down:
            call(self, depth)
        if sort_func == 'name':
            sort_func = by_name
        if sort_func:
            childrens = sorted(self._children, key=sort_func)
        else:
            childrens = self._children
        for _ in childrens:
            if hasattr(_, 'walk'):
                _.walk(callback, top_down, depth+1, sort_func, cls_filter)
            else:
                call(_, depth+1)
        if not top_down:
            call(self, depth)

    ##############################################

    @property
    def size_accumulator(self) -> int:
        return self._size_accumulator

    @property
    def file_accumulator(self) -> int:
        return self._file_accumulator

    def clear_size_accumulator(self) -> None:
        self._size_accumulator = 0

    def accumulate_size(self, *args, **kwargs) -> None:
        self._size_accumulator = self.disk_size
        for child in self._children:
            match child:
                case Directory():
                    _ = child.size_accumulator
                case File():
                    _ = child.disk_size
            self._size_accumulator += _

    def update_size_accumulator(self) -> None:
        self.walk(
            Directory.accumulate_size,
            top_down=False,
            cls_filter=Directory,
        )

    def accumulate_file(self, *args, **kwargs) -> None:
        self._file_accumulator = 0
        for _ in self._children:
            if isinstance(_, File):
                self._file_accumulator += 1

    def update_file_accumulator(self) -> None:
        self.walk(
            Directory.accumulate_file,
            top_down=False,
            cls_filter=Directory,
        )

####################################################################################################

class File(Node):

    ##############################################

    def __init__(self, path: Path) -> None:
        super().__init__(path)

    ##############################################

    def __repr__(self) -> str:
        return f'{self._path}'

####################################################################################################

class Walker(WalkerAbc):

    ##############################################

    def on_directory(self, dirpath: Path, dirname: str) -> None:
        path = dirpath.joinpath(dirname)
        # print(path)
        Directory(path)

    ##############################################

    def on_filename(self, dirpath: Path, filename: str) -> None:
        path = dirpath.joinpath(filename)
        # print('  ', path)
        File(path)
