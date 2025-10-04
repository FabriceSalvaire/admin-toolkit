####################################################################################################
#
# -
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

__all__ = ['File', 'Directory']

####################################################################################################

import pathlib

####################################################################################################

class Path:

    ##############################################

    @classmethod
    def make(self, path: str) -> 'Path':
        path = pathlib.Path(path)
        if path.is_file(follow_symlinks=False):
            return File(path)
        elif path.is_dir(follow_symlinks=False):
            return Directory(path)
        elif path.is_symlink():
            return Symlink(path)
        else:
            # is_junction
            # is_mount
            # is_socket
            # is_fifo
            # is_block_device
            # is_char_device
            return Special(path)

    ##############################################

    def __init__(self, path: str) -> None:
        self._path = pathlib.Path(path)

    ##############################################

    def __repr__(self) -> str:
        return str(self._path)

    @property
    def name(self) -> str:
        return self._path.name

    @property
    def parent_str(self) -> str:
        return str(self._path.parent)

    @property
    def parts(self) -> list[str]:
        return self._path.parts

####################################################################################################

class File(Path):
    pass

####################################################################################################

class Directory(Path):
    pass

####################################################################################################

class Symlink(Path):
    pass

####################################################################################################

class Special(Path):
    pass
