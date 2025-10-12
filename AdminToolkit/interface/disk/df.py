####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ =  ['df']

####################################################################################################

from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import math

from AdminToolkit.config import common_path as cp
from AdminToolkit.common.format import byte_humanize
from AdminToolkit.common.object import split_line
from AdminToolkit.common.subprocess import iter_on_command_output

####################################################################################################

EXCLUDED_FS_TYPES = (
    'devtmpfs',
    'efivarfs',
    'tmpfs',
)

####################################################################################################

@dataclass
class DfInfo:

    """Class to store the output of `df` for a filesystem"""

    # df sorted
    dev: str
    size: int
    used: int
    free: int
    pused: int
    mountpoint: str

    ##############################################

    @property
    def hsize(self) -> str:
        return byte_humanize(self.size)

    @property
    def hused(self) -> str:
        return byte_humanize(self.used)

    @property
    def hfree(self) -> str:
        return byte_humanize(self.free)

    @property
    def free_real(self) -> str:
        return self.size - self.used

    @property
    def hfree_real(self) -> str:
        return byte_humanize(self.free_real)

    @property
    def free_real_ratio(self) -> int:
        return math.ceil(self.free / self.free_real * 100)

    @property
    def pused_real(self) -> int:
        return math.ceil(self.used / self.size * 100)

####################################################################################################

def df() -> list[DfInfo]:
    """Run `df` and return a list of `DfInfo` instances"""
    df_infos = []
    cmd = [cp.DF]
    for _ in EXCLUDED_FS_TYPES:
        cmd.append(f'--exclude-type={_}')
    for line in iter_on_command_output(cmd, skip_first_lines=1):
        _ = split_line(
            line,
            filters=(
                ((0, 5), lambda _: Path(_)),
                ([1, 3], lambda _: int(_) * 1024),
                (4, lambda _: int(_.replace('%', ''))),
            ),
        )
        df_info = DfInfo(*_)
        # print(df_info)
        parts = df_info.mountpoint.parts
        # if (df_info.mountpoint == cp.ROOT
        #     or (len(parts) > 1 and parts[1] not in EXCLUDED_MOUNTPOINTS)):
        #     if len(parts) >= 2 and parts[1] == 'run':
        #         if not (len(parts) >= 3 and parts[2] == 'media'):
        #             continue
        df_infos.append(df_info)
    return df_infos

####################################################################################################


if __name__ == '__main__':
    _ = df()
    pprint(_)
