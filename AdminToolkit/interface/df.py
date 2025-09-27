####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint
import subprocess

####################################################################################################

DF = '/usr/bin/df'

####################################################################################################

def df() -> list:
    DfInfo = namedtuple('DfInfo', ('dev', 'size', 'used', 'free', 'pused', 'mountpoint'))
    cmd = (
        DF,
    )
    process = subprocess.run(cmd, capture_output=True)
    _ = process.stdout.decode('utf8')
    mount_points = []
    for i, line in enumerate(_.splitlines()):
        if not i:
            continue
        _ = [_ for _ in line.split()]
        for i in (0, 5):
            _[i] = Path(_[i])
        for i in range(1, 4):
            _[i] = int(_[i]) * 1024
        _[4] = int(_[4].replace('%', ''))
        df_info = DfInfo(*_)
        # print(df_info)
        parts = df_info.mountpoint.parts
        if (str(df_info.mountpoint) == '/'
            or (len(parts) > 1 and parts[1] not in ('dev', 'sys', 'run', 'tmp'))):
            mount_points.append(df_info)
    return mount_points

####################################################################################################


if __name__ == '__main__':
    _ = df()
    pprint(_)
