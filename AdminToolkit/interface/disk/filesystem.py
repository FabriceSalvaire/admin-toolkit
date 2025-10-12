####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['']

####################################################################################################

# from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
import calendar

from AdminToolkit.config import common_path as cp
from AdminToolkit.common.subprocess import iter_on_command_output

####################################################################################################

MONTH_MAP = {_[:3]: i for i, _ in enumerate(calendar.month_name)}

####################################################################################################

class DeviceFilesystem:

    ##############################################

    def __init__(self, device) -> None:
        self._device = device

####################################################################################################

# @dataclass
class Ext4DeviceFilesystem(DeviceFilesystem):

    # block_count = int
    # block_size = int
    # blocks_per_group = int
    # check_interval = str
    # checksum = str
    # checksum_type = str
    # default_directory_hash = str
    # default_mount_options = str
    # desired_extra_isize = int
    # directory_hash_seed = str
    # errors_behavior = str
    # fast_commit_length = int
    # filesystem_created = datetime
    # filesystem_features = str
    # filesystem_flags = str
    # filesystem_magic_number = str
    # filesystem_os_type = str
    # filesystem_revision = str
    # filesystem_state = str
    # filesystem_uuid = str
    # first_block = int
    # first_inode = int
    # first_orphan_inode = int
    # flex_block_group_size = int
    # fragment_size = int
    # fragments_per_group = int
    # free_blocks = int
    # free_inodes = int
    # group_descriptor_size = int
    # inode_blocks_per_group = int
    # inode_count = int
    # inode_size = int
    # inodes_per_group = int
    # journal_backup = str
    # journal_checksum = str
    # journal_checksum_type = str
    # journal_features = str
    # journal_inode = int
    # journal_sequence = str
    # journal_start = int
    # last_checked = datetime
    # last_mount_time = datetime
    # last_mounted_on = datetime
    # last_write_time = str
    # lifetime_writes = str
    # max_transaction_length = int
    # maximum_mount_count = int
    # mount_count = int
    # overhead_clusters = int
    # required_extra_isize = int
    # reserved_block_count = int
    # reserved_blocks_gid = str
    # reserved_blocks_uid = str
    # reserved_gdt_blocks = int
    # total_journal_blocks = int
    # total_journal_size = int

    ##############################################

    # @classmethod
    # def make(cls) -> 'Ext4DeviceFilesystem':

    ##############################################

    def __init__(self, device) -> None:
        super().__init__(device)
        self._dumpe2fs()

    ##############################################

    def _dumpe2fs(self) -> None:
        cmd = (
            cp.DUMPE2FS,
            '-h',
            self._device # .dev_path,
        )
        # data = {}
        for i, line in enumerate(iter_on_command_output(cmd)):
            # print(line)
            if i == 0:
                continue
            j = line.find(':')
            key = line[:j]
            value = line[j+1:].strip()
            try:
                value = int(value)
            except ValueError:
                pass
            key = key.lower()
            key = key.replace('#', '').strip()
            key = key.replace(' ', '_')
            match key:
                case  'check_interval' | 'filesystem_revision' | 'reserved_blocks_gid' | 'reserved_blocks_uid':
                    value = int(value[:value.find(' (')])
                case 'default_mount_options' | 'filesystem_features' | 'journal_features':
                    value = value.split()
                case 'filesystem_created' | 'last_checked' | 'last_mount_time' | 'last_write_time':
                    _, month, day, time_, year = value.split()
                    month = MONTH_MAP[month]
                    hour, minute, second = [int(_) for _ in time_.split(':')]
                    date = datetime(
                        year=int(year), month=month, day=int(day),
                        hour=hour, minute=minute, second=second,
                    )
                    value = date
            # print(key, value)
            setattr(self, key, value)
        #     data[key] = value
        # return data

####################################################################################################


if __name__ == '__main__':
    _ = Ext4DeviceFilesystem('/dev/mapper/vg--mx500--1-home')
    print('reserved_block_count:', _.reserved_block_count)
