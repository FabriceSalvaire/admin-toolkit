####################################################################################################

__all__ = ['mount', 'get_root_device']

####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.tools.parse import split_line
from AdminToolkit.tools.subprocess import run_command, iter_on_command_output

####################################################################################################

MOUNT = '/usr/bin/mount'
PROC_MOUNT = '/proc/self/mounts'
VGS = '/usr/bin/vgs'

####################################################################################################

def mount() -> list:
    MountInfo = namedtuple('MountInfo', ('dev', 'mountpoint', 'type', 'options'))
    cmd = (
        MOUNT,
    )
    mount_points = []
    for line in iter_on_command_output(cmd):
        if line.startswith('/dev'):
            _ = split_line(
                line,
                filters=(
                    ((0, 2), lambda _: Path(_)),
                ),
                skip=(1, 3),
            )
            # print(_)
            mountinfo = MountInfo(*_)
            mount_points.append(mountinfo)
    return mount_points

####################################################################################################    return mount_points

def proc_mount() -> list:
    ProcMountInfo = namedtuple('ProcMountInfo', ('dev', 'mountpoint', 'type', 'options', 'fs_freq', 'fs_passno'))
    _ = Path(PROC_MOUNT).read_text()
    mount_points = []
    for line in _.splitlines():
        if line.startswith('/dev'):
            _ = split_line(
                line,
                filters=(
                    ((0, 1), lambda _: Path(_)),
                ),
            )
            # print(_)
            mountinfo = ProcMountInfo(*_)
            mount_points.append(mountinfo)
    return mount_points

####################################################################################################

def get_root_device() -> str:
    from .partition import partion_to_device
    ### SECURITY FUNCTION ! ###
    for mount_info in proc_mount():
        # ROOT = Path('/')
        if str(mount_info.mountpoint) == '/':
            device = mount_info.dev
            #!# device = Path('/dev/sda1')
            # print(device)
            if str(device).startswith('/dev/mapper/'):
                # LVM
                parts = device.name.split('--')
                parts[-1] = parts[-1].split('-')[0]
                vg_name = '-'.join(parts)
                # print(vg_name)
                raise_if_not_root()
                cmd = (
                    VGS,
                    '--rows',
                    '--options=pv_name',
                    vg_name,
                )
                # print(cmd)
                _ = run_command(cmd)
                _, pvs = _.split()
                # pvs = ['/dev/sda1', '/dev/sda23']
                # pvs = ['/dev/sda1', '/dev/sdb23']
                # pvs = ['/dev/sda1', '/dev/sdb23', '/dev/sdc5']
                if _ != 'PV':
                    raise NameError('vgs output {_} {pvs}')
                match pvs:
                    case str():
                        return partion_to_device(pvs)
                    case list():
                        return set([partion_to_device(_) for _ in pvs])
                    case _:
                        raise NameError('vgs output {pvs}')
            elif str(device).startswith('/dev/sd'):
                return partion_to_device(device.name)
            else:
                raise NameError('Unsupported device {device}')

####################################################################################################


if __name__ == '__main__':
    _ = mount()
    pprint(_)

    print()
    _ = proc_mount()
    pprint(_)

    print()
    print('root is', get_root_device())
