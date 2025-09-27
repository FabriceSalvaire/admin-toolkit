####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint
import subprocess

####################################################################################################

MOUNT = '/usr/bin/mount'
PROC_MOUNT = '/proc/self/mounts'

####################################################################################################

def mount() -> list:
    MountInfo = namedtuple('MountInfo', ('dev', 'mountpoint', 'type', 'options'))
    cmd = (
        MOUNT,
    )
    process = subprocess.run(cmd, capture_output=True)
    _ = process.stdout.decode('utf8')
    mount_points = []
    for line in _.splitlines():
        if line.startswith('/dev'):
            _ = [_ for _ in line.split() if _ not in ('on', 'type')]
            # print(_)
            mountinfo = MountInfo(*_)
            mount_points.append(mountinfo)
    return mount_points

####################################################################################################    return mount_points

def proc_mount() -> list:
    MountInfo = namedtuple('MountInfo', ('dev', 'mountpoint', 'type', 'options', 'fs_freq', 'fs_passno'))
    _ = Path(PROC_MOUNT).read_text()
    mount_points = []
    for line in _.splitlines():
        if line.startswith('/dev'):
            _ = [_ for _ in line.split()]
            # print(_)
            mountinfo = MountInfo(*_)
            mount_points.append(mountinfo)
    return mount_points

####################################################################################################


if __name__ == '__main__':
    _ = mount()
    pprint(_)
    _ = proc_mount()
    pprint(_)
