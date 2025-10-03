####################################################################################################

__all__ = ['Devices']

####################################################################################################

from collections import namedtuple
from pprint import pprint
import getpass
import inspect
import os
import traceback

from pathlib import Path

from AdminToolkit.cli import CommandGroup
from AdminToolkit.interface.disk.tool import to_dev_path
from AdminToolkit.tools.format import byte_humanize, fix_none, Table

####################################################################################################

class Devices(CommandGroup):

    ##############################################

    def devices(self) -> None:
        from AdminToolkit.interface.disk.device import BlockDevice
        devices = BlockDevice.devices()
        for device in sorted(devices, key=lambda _: _.name):
            self.print()
            self.print(f'<blue>{device.name}</blue>')
            self.print(f'  {device.model}   {device.hsize}')
            if device.removable:
                self.print(f'  Removable')
            for link in device.links:
                if link.parent.name == 'by-id' and link.name[:3] not in ('wwn',):
                    self.print(f'  <green>{link}</green>')
            # for part in device.partitions:
            #     ro = '<red>RO</red>' if part.ro else ''
            #     self.print(f'  <blue>{part.name:6}</blue>  {part.hsize}  {ro}')
            #     for mountpoint in part.mountpoints:
            #         self.print(f'    <green>{mountpoint}</green>')

    ##############################################

    def is_root(self, name: str) -> None:
        from AdminToolkit.danger import raise_if_root_device, AbortAction
        try:
            raise_if_root_device(name)
            self.print('is <green>safe</green> device')
        except AbortAction:
            self.print('is <red>root</red> device')

    ##############################################

    def clear_device(self, dev_path: str) -> None:
        from AdminToolkit.interface.disk.partition import clear_device
        clear_device(dev_path)   # , print_output=True

    ##############################################

    def parts(self, dev_path: str) -> None:
        from AdminToolkit.interface.disk.device import BlockDevice
        device = BlockDevice(dev_path)
        self.print(f'<blue>{device.name}</blue> -> <blue>{device.resolved_dev_path}</blue>')
        self.print(f'  {device.model}   <blue>{device.hsize}</blue> = {device.number_of_sectors:_} s')
        self.print(f'  Partition Table: <green>{device.partition_table_type}</green>')
        # pprint(device._lsblk)
        # pprint(device._gpt)
        last_end = 0
        def print_line(**d):
            d = namedtuple('PartPrintLine', d.keys())(**d)
            # pprint(d)
            self.print(f'<red>{d.name:5}</red> | {d.start:14_} — {d.end:14_} = {d.size:16_} = <blue>{d.hsize:>8}</blue> | {d.fs:4} | {d.mountpoint:16} | {d.label}')
        def print_gap(start):
            if start != last_end + 1:
                gap_size = device.sector_to_byte(start - last_end)
                hgap_size = byte_humanize(gap_size)
                print_line(
                    name='...',
                    start=last_end + 1 if last_end else 0,
                    end=start - 1,
                    size=gap_size,
                    hsize=hgap_size,
                    label='',
                    fs='',
                    mountpoint='',
                )
        for p in sorted(device.partitions, key=lambda p: p.gpt_start):
            # pprint(p._lsblk)
            # pprint(p._gpt)
            print_gap(p.gpt_start)
            print_line(
                name=p.name,
                start=p.gpt_start,
                end=p.gpt_end,
                size=p.gpt_size,
                hsize=p.gpt_hsize,
                # label=p.label,
                label=p.part_label,
                fs=p.filesystem.replace('_member', ''),
                mountpoint=fix_none(p.mountpoint),
            )
            last_end = p.gpt_end
        print_gap(device.number_of_sectors)

    ##############################################

    def partfs(self, dev_path: str) -> None:
        from AdminToolkit.interface.disk.device import BlockDevice
        device = BlockDevice(dev_path)
        self.print(f'<blue>{device.name}</blue>')
        self.print(f'  {device.model}   <blue>{device.hsize}</blue>')
        table = Table(
            format={
                'name': '<red>{}</red>',
                'fs': '{}',
                'mount': '<green>{}</green>',
                'part_label': '{}',
                'label': '{}',
                'size': '{}',
                'used': '{}',
                'pused': '{}',
            },
            header={
                'name': 'Name',
                'fs': 'Fs',
                'mount': 'Mount',
                'part_label': 'Part Label',
                'label': 'Label',
                'size': 'Size',
                'used': 'Used',
                'pused': '%',
            },
        )
        for p in sorted(device.partitions, key=lambda p: p.number):
            table.append(
                name=p.name,
                fs=p.filesystem.replace('_member', ''),
                mount=fix_none(p.mountpoint),
                part_label=p.part_label,
                label=p.label,
                size=p.fs_hsize,
                used=p.fs_hused,
                pused=p.fs_pused,
            )
        self.print(table)

    ##############################################

    def df(self) -> None:
        from AdminToolkit.interface.disk.df import df
        df_infos = df()
        self.print(f'{"":30} {"Size":>8} {"Used":>8} {"Free":>8}')
        for d in sorted(df_infos, key=lambda _: str(_.mountpoint)):
            mountpoint = str(d.mountpoint)
            free = d.hfree
            if free.endswith('MB') or free.endswith('KB'):
                self.print(f'<red>{mountpoint:30}</red> {d.hsize:>8} {d.hused:>8} <red>{free:>8}</red> {d.pused:>3}%   {d.dev}')
            else:
                self.print(f'<green>{mountpoint:30}</green> {d.hsize:>8} {d.hused:>8} {free:>8} {d.pused:>3}%   {d.dev}')

    ##############################################

    def _load_backup_config(self) -> dict:
        import yaml
        config_path = SOURCE_PATH.joinpath('backup', 'config.yaml')
        backup_config = yaml.load(config_path.read_text(), Loader=yaml.SafeLoader)
        return backup_config

    ##############################################

    def _backup_config(self, name: str) -> list[Path]:
        backup_config = self._load_backup_config()
        config = backup_config[name]
        backup_path = config['backup_path']
        filter_path = SOURCE_PATH.joinpath('backup', 'filters', config['filter'])
        return backup_path, filter_path

    ##############################################

    def check_rsync_filter(self, name: str) -> None:
        from AdminToolkit.backup.rsync import RsyncBackup
        _, filter_path = self._backup_config(name)
        self.print(f"Filter is <green>{filter_path}</green>")
        RsyncBackup.check_filter(filter_path)

    ##############################################

    def backup(self, name: str) -> None:
        from AdminToolkit.backup.rsync import RsyncBackup
        backup_path, filter_path = self._backup_config(name)
        self.print(f"Backup target is <green>{backup_path}</green>")
        self.print(f"Filter is <green>{filter_path}</green>")
        _ = RsyncBackup(backup_path, filter_path)
        _.run()
