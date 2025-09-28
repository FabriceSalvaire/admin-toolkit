####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from AdminToolkit.tools.format import byte_humanize
from AdminToolkit.tools.parse import split_line
from AdminToolkit.tools.subprocess import iter_on_command_output

####################################################################################################

DF = '/usr/bin/df'

ROOT = Path('/')
EXCLUDED_MOUNTPOINTS = ('dev', 'sys', 'tmp')

####################################################################################################

DfInfoBase = namedtuple(
    'DfInfoBase', (
        'dev',
        'size',
        'used',
        'free',
        'pused',
        'mountpoint',
    ),
)

class DfInfo(DfInfoBase):

    @property
    def hsize(self) -> str:
        return byte_humanize(self.size)

    @property
    def hused(self) -> str:
        return byte_humanize(self.used)

    @property
    def hfree(self) -> str:
        return byte_humanize(self.free)

####################################################################################################


def df() -> list:
    df_infos = []
    cmd = (
        DF,
    )
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
        if (df_info.mountpoint == ROOT
            or (len(parts) > 1 and parts[1] not in EXCLUDED_MOUNTPOINTS)):
            if len(parts) > 2 and parts[1] == 'run' and parts[2] != 'media':
                continue
            df_infos.append(df_info)
    return df_infos

####################################################################################################


if __name__ == '__main__':
    _ = df()
    pprint(_)
