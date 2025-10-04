####################################################################################################

__all__ = ['Filesystem']

####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from AdminToolkit.cli import CommandGroup, DirectoryPath
from AdminToolkit.tools.format import byte_humanize

####################################################################################################

class Filesystem(CommandGroup):

    ##############################################

    def du(self, path: DirectoryPath) -> None:
        pass
