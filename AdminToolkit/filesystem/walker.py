####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from pathlib import Path
from typing import AnyStr, List

# import os
# from os import PathLike

from AdminToolkit.printer import atprint

####################################################################################################

class WalkerAbc:

    """Base class to implement a walk in a file hierarchy."""

    ##############################################

    def __init__(self, path: AnyStr | Path) -> None:
        # Make the path absolute, resolving any symlinks.
        self._path = Path(path).expanduser().resolve()
        if Path(path) != self._path:
            atprint(f"Resolved to {self._path}")
        if not self._path.exists():
            raise ValueError(f"Path {path} doesn't exists")

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    ##############################################

    def run(self,
            top_down: bool = False,
            sort: bool = False,
            follow_symlinks: bool = False,
            max_depth: int = -1,
            ) -> None:
        if max_depth >= 0:
            top_down = True
            depth = 0
        # to avoid UnicodeEncodeError: surrogates not allowed
        # top = str(self._path).encode('utf-8')
        # for dirpath, dirnames, filenames in os.walk(top, topdown=top_down, followlinks=follow_links):
        # https://docs.python.org/3/library/pathlib.html#pathlib.Path.walk

        def on_error(exception):
            # exception.filename, 
            print(exception)

        for dirpath, dirnames, filenames in self._path.walk(top_down=top_down, on_error=on_error, follow_symlinks=follow_symlinks):
            # dirnames and filenames are List[bytes]
            if top_down and sort:
                self.sort_dirnames(dirnames)
            if hasattr(self, 'on_directory'):
                for directory in dirnames:
                    self.on_directory(dirpath, directory)
            if hasattr(self, 'on_filename'):
                for filename in filenames:
                    self.on_filename(dirpath, filename)
            if max_depth >= 0:
                depth += 1
                if depth > max_depth:
                    break

    ##############################################

    def sort_dirnames(self, dirnames: List[bytes]) -> None:
        # Fixme: sort utf-8 bytes ???
        dirnames.sort()

    ##############################################

    # def on_directory(self, dirpath: bytes, dirname: bytes) -> None:
    #     raise NotImplementedError

    ##############################################

    # def on_filename(self, dirpath: bytes, filename: bytes) -> None:
    #     raise NotImplementedError
