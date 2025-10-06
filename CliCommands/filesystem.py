####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['Filesystem']

####################################################################################################

from pathlib import Path
from pprint import pprint
import math

from AdminToolkit.cli import CommandGroup, DirectoryPath, FilePath
from AdminToolkit.config import units
from AdminToolkit.tools.format import byte_humanize

####################################################################################################

class Filesystem(CommandGroup):

    ##############################################

    def du(self, path: DirectoryPath) -> None:
        from AdminToolkit.filesystem.tree import Walker, Directory

        root = Path(path).expanduser().resolve()
        if Path(path) != root:
            self.print(f"Resolved to {root}")

        self.print('walk on disk...')
        root_node = Directory(root, root=True)
        walker = Walker(root)
        walker.run(
            top_down=True,
            sort=False,
            follow_symlinks=False,
            max_depth=-1,
        )
        self.print('done')

        self.print('accumulate...')
        root_node.update_size_accumulator()
        self.print('done')

        self._cache.store('root_node', root_node)

    ##############################################

    def du_save(self, path: FilePath) -> None:
        self.save_cache('root_node', path)

    def du_load(self, path: FilePath) -> None:
        self.load_cache('root_node', path)

    def du_reset(self) -> None:
        self.cache.reset_cache('root_node')

    ##############################################

    def du_exam(self, depth_max: int, size_min: str = 'GB') -> None:
        from AdminToolkit.filesystem.tree import Directory

        root_node = self._cache.get('root_node')
        if root_node is None:
            return

        depth_max = int(depth_max)

        for i, c in enumerate(size_min):
            if not c.isnumeric():
                break
        _size_min = size_min[:i]
        unit = size_min[i:]
        print(_size_min, unit)
        if _size_min:
            _size_min = float(_size_min)
        match unit:
            case 'kB':
                unit = units.KB
            case 'MB':
                unit = units.MB
            case 'GB':
                unit = units.GB
            case '':
                unit = 1
            case _:
                raise ValueError(f"Invalid unit {size_min}")
        _size_min *= unit

        # print(depth_max, _size_min)

        class Toggle:
            def __init__(self):
                self._value = False
            def __bool__(self):
                return self._value
            def toggle(self):
                self._value = not self._value
        colour = Toggle()

        def show(node, depth):
            if depth <= depth_max and node.size_accumulator >= _size_min:
                # self.print(' '*4*depth + f"{node.path.name} {size}")
                L = 50
                # Fixme: strip large name
                name = node.path.name
                if len(name) > 16:
                    name = name[:16]
                left = ' '*4*depth + name
                if colour:
                    _ = '.'*(L - len(left))
                    left = left + _
                size = byte_humanize(node.size_accumulator)
                right = '='*math.ceil(50 * node.size_accumulator / root_node.size_accumulator)
                # if colour:
                #     co = '<green>'
                #     cp = '</green>'
                # else:
                co = ''
                cp = ''
                line = f"{co}{left:50} {size:>7}   {right}{cp}"
                self.print(line)
                colour.toggle()

        root_node.walk(
            callback=show,
            top_down=True,
            sort_func='name',
            cls_filter=Directory,
        )
