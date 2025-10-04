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
from AdminToolkit.config import unit
from AdminToolkit.tools.format import byte_humanize

####################################################################################################

class Filesystem(CommandGroup):

    ##############################################

    def du(self, path: DirectoryPath) -> None:
        from AdminToolkit.filesystem.tree import Walker, Directory

        root = Path(path)

        print('walk on disk...')
        root_node = Directory(root, root=True)
        walker = Walker(root)
        walker.run(
            top_down=True,
            sort=False,
            follow_symlinks=False,
            max_depth=-1,
        )
        print('done')

        print('accumulate...')
        root_node.update_size_accumulator()
        print('done')

        def show(node, depth):
            if depth <= 3 and node.size_accumulator >= unit.GB:
                # print(' '*4*depth + f"{node.path.name} {size}")
                left = ' '*4*depth + node.path.name
                size = byte_humanize(node.size_accumulator)
                right = '='*math.ceil(50 * node.size_accumulator / root_node.size_accumulator)
                print(f"{left:50}   {size:>10}   {right}")

        root_node.walk(
            callback=show,
            top_down=True,
            sort_func='name',
            cls_filter=Directory,
        )
