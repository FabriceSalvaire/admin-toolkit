####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = []

####################################################################################################

# from pprint import pprint
from typing import Iterator

from AdminToolkit.config import common_path as cp

####################################################################################################

class LineParser:

    ##############################################

    def __init__(self, content: str, separator: str = ':') -> None:
        self._content = str(content)
        self._separator = str(separator)

        for line in self.yield_line():
            self.on_line(line)

    ##############################################

    def yield_line(self) -> Iterator[str]:
        for line in self._content.splitlines():
            line = line.strip()
            if line:
                yield line

    ##############################################

    def on_line(self, line: str) -> None:
        sep_index = line.find(self._separator)
        if sep_index == -1:
            raise ValueError(line)
        left = line[:sep_index].strip()
        right = line[sep_index+1:].strip()
        left = self.to_key(left)
        right = self.to_value(left, right)
        # print(left, type(right), right)

    ##############################################

    def to_key(self, left: str) -> str:
        return left.lower().replace(' ', '_')

    ##############################################

    def to_value(self, left: str, right: str) -> str:
        if not right:
            return None
        if ' ' in right:
            return [self.to_value(left, _) for _ in right.split()]
        if '.' in right:
            try:
                return float(right)
            except ValueError:
                pass
        if right[0].isnumeric() and right[-1].isnumeric():
            try:
                return int(right)
            except ValueError:
                pass
        match right.lower():
            case 'yes' | 'true':
                return True
            case 'no' | 'false':
                return False
        return right

####################################################################################################

def cpuinfo():
    content = cp.PROC_CPUINFO.read_text()
    _ = LineParser(content)

####################################################################################################


if __name__ == '__main__':
    cpuinfo()
