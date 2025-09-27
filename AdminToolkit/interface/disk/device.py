####################################################################################################

"""dev interface

"""

__all__ = ['Device', 'devices']

####################################################################################################

# lsblk
# hdparm -i /dev/sda

####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint
from typing import Iterator

import json
import subprocess

from AdminToolkit.interface.user import RootPermissionRequired
from AdminToolkit.tools.format import byte_humanize, fix_none
from AdminToolkit.tools.dict import bool_from_json, fix_dict_key
from .partition import parted
from .tool import to_dev_path, is_sd

####################################################################################################

LSBLK = '/usr/bin/lsblk'

SYS_BLOCK = Path('/sys/block')
DEV_DISK = Path('/dev/disk')

LSBLK_FIELDS = (
    'alignment',
    'children',
    'dax',
    'disc_aln',
    'disc_gran',
    'disc_max',
    'disc_zero',
    'disk_seq',
    'fsavail',
    'fsroots',
    'fssize',
    'fstype',
    'fsusep',
    'fsused',
    'fsver',
    'group',
    'hctl',
    'hotplug',
    'id',
    'id_link',
    'kname',
    'label',
    'log_sec',
    'maj',
    'maj_min',
    'min',
    'min_io',
    'mode',
    'model',
    'mountpoint',
    'mountpoints',
    'mq',
    'name',
    'opt_io',
    'owner',
    'partflags',
    'partlabel',
    'partn',
    'parttype',
    'parttypename',
    'partuuid',
    'path',
    'phy_sec',
    'pkname',
    'pttype',
    'ptuuid',
    'ra',
    'rand',
    'rev',
    'rm',
    'ro',
    'rota',
    'rq_size',
    'sched',
    'serial',
    'size',
    'start',
    'state',
    'subsystems',
    'tran',
    'type',
    'uuid',
    'vendor',
    'wsame',
    'wwn',
    'zone_amax',
    'zone_app',
    'zone_nr',
    'zone_omax',
    'zone_sz',
    'zone_wgran',
    'zoned',
)

####################################################################################################

def from_lsblk_dict(d: dict):
    LsblkData = namedtuple('LsblkData', LSBLK_FIELDS, defaults=[None]*len(LSBLK_FIELDS))
    fix_dict_key(d)
    for key, value in d.items():
        if isinstance(value, (str)):
            if value in ('true', 'false'):
                d[key] = bool_from_json(value)
    if 'children' in d:
        d['children'] = [from_lsblk_dict(_) for _ in d['children']]
    return LsblkData(**d)

def lsblk(dev_path: str | Path) -> dict:
    # sblk command reads the sysfs filesystem and udev db to gather
    # information. If the udev db is not available or lsblk is
    # compiled without udev support, then it tries to read LABELs,
    # UUIDs and filesystem types from the block device. In this case
    # root permissions are necessary.
    dev_path = to_dev_path(dev_path)
    cmd = (
        LSBLK,
        '--bytes',
        '--output-all',
        '--json',
        str(dev_path),
    )
    process = subprocess.run(cmd, capture_output=True)
    _ = process.stdout.decode('utf8')
    try:
        data = json.loads(_)
    except json.decoder.JSONDecodeError:
        raise NameError(f'{cmd} -> {_}')
    _ = data['blockdevices'][0]
    _ = from_lsblk_dict(_)
    return _

####################################################################################################

def dev_links(name: str) -> list[Path]:
    links = []
    for root, _, files in DEV_DISK.walk():
        root = Path(root)
        for filename in files:
            link = root.joinpath(filename)
            if link.is_symlink():
                _ = link.readlink().name
                if _ == name:
                    links.append(link)
    links.sort(key=lambda _: str(_))
    return links

####################################################################################################

class BlockDevice:

    ##############################################

    def __init__(self, dev_path: str | Path) -> None:
        self.dev_path = to_dev_path(dev_path)
        self._lsblk = lsblk(self.dev_path)
        self._read_gpt_table()
        self.partitions = [Partition(self, _) for _ in self._lsblk.children]
        self.links = dev_links(self.name)

    ##############################################

    # def _get_partitions(self) -> None:
    #     self._partitions = []
    #     for _ in Path(f'/sys/block/{self.name}').iterdir():
    #         if _.name.startswith(self.name):
    #             part = Partition(self, _.name)
    #             self._partitions.append(part)
    #     self._partitions.sort(key=lambda _: _.id)

    ##############################################

    def _read_gpt_table(self):
        try:
            self._gpt = parted(self.dev_path)
            self.is_gpt = self._gpt.label == 'gpt'
            self._gpt_partitions = {_.number: _ for _ in self._gpt.partitions}
        except RootPermissionRequired:
            self._gpt = None
            self.is_gpt = None
            self._gpt_partitions = None

    ##############################################

    @property
    def name(self) -> bool:
        return self.dev_path.name

    @property
    def resolved_dev_path(self) -> bool:
        return to_dev_path(self.dev_path, resolve=True)

    @property
    def is_sd(self) -> bool:
        return is_sd(self.name)

    ##############################################

    @property
    def model(self) -> str:
        # return Path(f'/sys/block/{self.name}/device/model').read_text().strip()
        return self._lsblk.model

    # @property
    # def vendor(self) -> str:
    #     return self._lsblk.vendor

    @property
    def removable(self) -> bool:
        return self._lsblk.rm

    @property
    def part_table_type(self) -> str:
        return self._lsblk.pttype

    @property
    def size(self) -> int:
        return self._lsblk.size

    @property
    def hsize(self) -> str:
        return byte_humanize(self.size)

    @property
    def number_of_sectors(self) -> int:
        return self._gpt.size

    ##############################################

    @property
    def partition_table_type(self) -> str:
        return self._gpt.label.upper()

    @property
    def sector_size(self) -> int:
        return self._gpt.logical_sector_size

    def sector_to_byte(self, value: int) -> int:
        return value * self.sector_size

####################################################################################################

class Partition:

    ##############################################

    def __init__(self, device: BlockDevice, lsblk: dict) -> None:
        self.device = device
        self._lsblk = lsblk
        # self.id == self.part_number
        if device._gpt_partitions is not None:
            self._gpt = device._gpt_partitions[self.number]
        else:
            # Fixme: raise ...
            self._gpt = None
        self.links = dev_links(self.name)

    ##############################################

    @property
    def name(self) -> int:
        return self._lsblk.name

    @property
    def id(self) -> int:
        _ = len(self.device.name)
        return int(self.name[_:])

    ##############################################

    # @property
    # def size(self) -> int:
    #     return int(Path(f'/sys/block/{self.device.name}/{self.name}/size').read_text()) * 512

    ##############################################

    @property
    def number(self) -> str:
        return self._lsblk.partn

    @property
    def part_label(self) -> str:
        return fix_none(self._lsblk.partlabel)

    @property
    def part_type(self) -> str:
        return self._lsblk.parttypename

    @property
    def part_flags(self) -> str:
        return self._lsblk.partflags

    @property
    def label(self) -> str:
        return fix_none(self._lsblk.label)

    @property
    def size(self) -> int:
        return self._lsblk.size

    @property
    def hsize(self) -> str:
        return byte_humanize(self.size)

    @property
    def type(self) -> str:
        return self._lsblk.type

    @property
    def mountpoint(self) -> str:
        return self._lsblk.mountpoint

    @property
    def mountpoints(self) -> [str]:
        _ = self._lsblk.mountpoints
        if len(_) == 1 and _[0] is None:
            return []
        return _

    @property
    def ro(self) -> bool:
        return self._lsblk.ro

    ##############################################

    @property
    def filesystem(self) -> str:
        # return self._gpt.filesystem
        return fix_none(self._lsblk.fstype)

    @property
    def fs_size(self) -> int:
        return self._lsblk.fssize

    @property
    def fs_hsize(self) -> int:
        return byte_humanize(self.fs_size)

    @property
    def fs_used(self) -> int:
        return self._lsblk.fsused

    @property
    def fs_hused(self) -> int:
        return byte_humanize(self.fs_used)

    @property
    def fs_pused(self) -> int:
        _ = self._lsblk.fsusep
        if _:
            return int(_[:-1])
        return None

    ##############################################

    @property
    def gpt_uuid(self) -> str:
        return self._gpt.uuid

    @property
    def gpt_start(self) -> int:
        return self._gpt.start

    @property
    def gpt_end(self) -> int:
        return self._gpt.end

    @property
    def gpt_size(self) -> int:
        return self.device.sector_to_byte(self._gpt.size)

    @property
    def gpt_hsize(self) -> int:
        return byte_humanize(self.gpt_size)

    @property
    def gpt_flags(self) -> [str]:
        return self._gpt.flags

####################################################################################################

def devices() -> Iterator[BlockDevice]:
    for _ in SYS_BLOCK.iterdir():
        if is_sd(_.name):
            device = BlockDevice(_.name)
            yield device
