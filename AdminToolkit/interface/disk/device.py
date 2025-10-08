####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""dev interface

"""

__all__ = ['BlockDevice']

####################################################################################################

# lsblk
# hdparm -i /dev/sda

####################################################################################################

from enum import IntEnum, auto
from pathlib import Path
# from pprint import pprint
from typing import Iterator

from AdminToolkit.config import common_path as cp
from AdminToolkit.interface.disk.partition import parted
from AdminToolkit.interface.disk.tool import to_dev_path, is_sd
from AdminToolkit.interface.user import RootPermissionRequired
from AdminToolkit.tools.format import byte_humanize, fix_none
from AdminToolkit.tools.object import namedtuple_factory
from AdminToolkit.tools.subprocess import run_command

####################################################################################################

LsblkData = namedtuple_factory(
    'LsblkData',
    (
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
    ))

####################################################################################################

def lsblk(dev_path: str | Path) -> dict:
    # lsblk command reads the sysfs filesystem and udev db to gather
    # information. If the udev db is not available or lsblk is
    # compiled without udev support, then it tries to read LABELs,
    # UUIDs and filesystem types from the block device. In this case
    # root permissions are necessary.
    dev_path = to_dev_path(dev_path)
    cmd = (
        cp.LSBLK,
        '--bytes',
        '--output-all',
        '--json',
        str(dev_path),
    )
    data = run_command(
        cmd,
        to_json=True,
        cls_map={'children': lambda value: [LsblkData(**_) for _ in value]},
    )
    _ = data['blockdevices'][0]
    return LsblkData(**_)

####################################################################################################

class DeviceType(IntEnum):
    SCSI_DEVICE = auto()
    SCSI_PARTITION = auto()
    LVM_LOGIC_VOLUME = auto()
    MDRAID_VOLUME = auto()

####################################################################################################

class DeviceAbc:

    ##############################################

    @classmethod
    def split_lvm(cls, dev_path: Path | str) -> [str, str]:
        _ = str(dev_path)
        if _.startswith('/dev/mapper/'):
            name = dev_path.name
            sep = None
            for i in range(1, len(name)):
                if name[i] == '-' and name[i+1] != '-' and name[i-1] != '-':
                    sep = i
            if sep is not None:
                vg_name = name[:sep]
                lv_name = name[sep+1:]
                return vg_name, lv_name
        return None

    ##############################################

    @classmethod
    def dev_path_type(cls, dev_path: Path | str) -> DeviceType:
        dev_path = Path(dev_path)
        if not dev_path.exists():
            raise ValueError(f"Device path {dev_path} doesn't exists")
        _ = str(dev_path)
        if _.startswith('/dev/sd'):
            if dev_path.name[-1].isnumeric():
                return DeviceType.SCSI_PARTITION
            else:
                return DeviceType.SCSI_DEVICE
        elif _.startswith('/dev/dm'):
            if dev_path.name.startswith('dm-'):
                return DeviceType.LVM_LOGIC_VOLUME
            else:
                return DeviceType.MDRAID_VOLUME
        elif _.startswith('/dev/mapper/'):
            if cls.split_lvm(dev_path) is not None:
                return DeviceType.LVM_LOGIC_VOLUME
        elif dev_path.is_simlink():
            target = dev_path.resolve()
            if str(target).startswith('/dev/dm-'):
                return DeviceType.LVM_LOGIC_VOLUME
        return None

   ##############################################

    @property
    def links(self) -> Iterator[str]:
        return iter(self._links)

   ##############################################

    def filtered_links(self, by: str = '', name: str = '') -> Iterator[str]:
        for _ in self._links:
            if by and f'by-{by}' != _.parts[3]:
                continue
            if name and name not in _.name:
                continue
            yield _

####################################################################################################

class BlockDevice(DeviceAbc):

    ##############################################

    @classmethod
    def devices(cls) -> Iterator['BlockDevice']:
        """Return an iterator on BlockDevice"""
        for _ in cp.SYS_BLOCK.iterdir():
            if is_sd(_.name):
                device = BlockDevice(_.name)
                yield device

    ##############################################

    @classmethod
    def dev_links(cls, name: str) -> list[Path]:
        """Return the list of links for a device"""
        links = []
        for root, _, files in cp.DEV_DISK.walk():
            root = Path(root)
            for filename in files:
                link = root.joinpath(filename)
                if link.is_symlink():
                    _ = link.readlink().name
                    if _ == name:
                        links.append(link)
        links.sort(key=lambda _: str(_))
        return links

    ##############################################

    def __init__(self, dev_path: str | Path) -> None:
        self._dev_path = to_dev_path(dev_path)
        # Fixme: can return None
        self._lsblk = lsblk(self.dev_path)
        self._read_gpt_table()
        # if self._lsblk is not None:
        self._partitions = [Partition(self, _) for _ in self._lsblk.children]
        # else:
        #     self.partitions = None
        self._links = self.dev_links(self.name)

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
            # Fixme: It creates a partition for MBR extended
            self._gpt_partitions = {_.number: _ for _ in self._gpt.partitions}
        except RootPermissionRequired:
            self._gpt = None
            self.is_gpt = None
            self._gpt_partitions = None

    ##############################################

    @property
    def dev_path(self) -> Path:
        return self._dev_path

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

    ##############################################

    @property
    def partitions(self) -> Iterator['Partition']:
        return iter(self._partitions)

####################################################################################################

class Partition(DeviceAbc):

    ##############################################

    def __init__(self, device: BlockDevice, lsblk: dict) -> None:
        self._device = device
        self._lsblk = lsblk
        # self.id == self.part_number
        if device._gpt_partitions is not None:
            self._gpt = device._gpt_partitions[self.number]
        else:
            # Fixme: raise ...
            self._gpt = None
        self._links = BlockDevice.dev_links(self.name)

    ##############################################

    @property
    def device(self) -> BlockDevice:
        return self._device

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
        _ = self._lsblk.partn
        # Debian
        if _ is None:
            return self.id
        return _

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
    def is_ebr(self) -> str:
        return self._gpt.type == 'extended'

    @property
    def gpt_uuid(self) -> str:
        return self._gpt.uuid

    @property
    def gpt_type_uuid(self) -> str:
        return self._gpt.type_uuid

    @property
    def gpt_type_uuid_str(self) -> str:
        return self._gpt.type_uuid_str

    @property
    def gpt_start(self) -> int:
        return self._gpt.start

    @property
    def gpt_end(self) -> int:
        return self._gpt.end

    @property
    def gpt_number_of_sectors(self) -> int:
        return self.gpt_end - self.gpt_start + 1

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

if __name__ == '__main__':
    devices = BlockDevice.devices()
    for device in devices:
        print(device.name)
        for link in device.links:
            print(' '*4, link)
        for partition in device.partitions:
            print(' '*2, partition.name)
            for link in partition.filtered_links(by='id', name='usb'):
                print(' '*4, link)
