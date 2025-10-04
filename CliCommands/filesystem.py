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

from AdminToolkit.cli import CommandGroup, DirectoryPath
from AdminToolkit.config import units
from AdminToolkit.tools.format import byte_humanize

####################################################################################################

class Filesystem(CommandGroup):

    root_node = None

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

        Filesystem.root_node = root_node

    ##############################################

    def du_reset(self) -> None:
        self.root_node = None

    ##############################################

    def du_exam(self, depth_max: int, size_min: str = 'GB') -> None:
        from AdminToolkit.filesystem.tree import Directory

        if Filesystem.root_node is None:
            return
        root_node = Filesystem.root_node

        depth_max = int(depth_max)

        for i, c in enumerate(size_min):
            if not c.isnumeric():
                break
        unit = size_min[i:]
        size_min = size_min[:i]
        if size_min:
            size_min = float(size_min)
        match unit:
            case 'KB':
                unit = units.KB
            case 'MB':
                unit = units.MB
            case 'GB':
                unit = units.GB
        size_min *= unit

        # print(depth_max, size_min)

        def show(node, depth):
            if depth <= depth_max and node.size_accumulator >= size_min:
                # self.print(' '*4*depth + f"{node.path.name} {size}")
                left = ' '*4*depth + node.path.name
                size = byte_humanize(node.size_accumulator)
                right = '='*math.ceil(50 * node.size_accumulator / root_node.size_accumulator)
                self.print(f"{left:50}   {size:>10}   {right}")

        root_node.walk(
            callback=show,
            top_down=True,
            sort_func='name',
            cls_filter=Directory,
        )
