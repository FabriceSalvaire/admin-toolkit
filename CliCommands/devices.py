####################################################################################################

__all__ = ['Devices']

####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from AdminToolkit.cli import CommandGroup, DevPath
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
        from AdminToolkit.danger import raise_if_root_device, IsRootAbortAction
        try:
            raise_if_root_device(name)
            self.print('is <green>safe</green> device')
        except IsRootAbortAction:
            self.print('is <red>root</red> device')

    ##############################################

    def clear_device(self, dev_path: DevPath) -> None:
        from AdminToolkit.interface.disk.partition import clear_device
        clear_device(dev_path)   # , print_output=True

    ##############################################

    def parts(self, dev_path: DevPath) -> None:
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

    def partfs(self, dev_path: DevPath) -> None:
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
        self.print(f'{"":30} {"Size":>8} {"Used":>8} {"Free":>8} {"Freal":>8} {"f/r":>4} {"used":>4}')
        for d in sorted(df_infos, key=lambda _: str(_.mountpoint)):
            mountpoint = str(d.mountpoint)
            if d.free != 0:
                free = d.hfree
            else:
                free = str(d.free) + 'KB'
            real_free = d.hfree_real
            ratio = f'{d.free_real_ratio}%'
            pused_real = f'{d.pused_real}%'
            if real_free == free:
                real_free = ''
                ratio = ''
                pused_real = ''
            if free.endswith('MB') or free.endswith('KB'):
                self.print(f'<red>{mountpoint:30}</red> {d.hsize:>8} {d.hused:>8} <red>{free:>8}</red> {real_free:>8} {ratio:>4} {d.pused:>3}% {pused_real:>4}  {d.dev}')
            else:
                self.print(f'<green>{mountpoint:30}</green> {d.hsize:>8} {d.hused:>8} {free:>8} {real_free:>8} {ratio:>4} {d.pused:>3}% {pused_real:>4}  {d.dev}')

    ##############################################

    def mdraid(self) -> None:
        from AdminToolkit.interface.disk.mdraid import MdRaidDevices
        for _ in MdRaidDevices():
            # pprint(_)
            self.print(f"MD {_.raid_type.upper()} <blue>{_.name}</blue>")
            self.print(f"  /dev/<green>{_.number_name}</green>")
            devices = ' '.join(_.devices.values())
            self.print(f"  devices: <green>{devices}</green>")

    ##############################################

    def lvm(self) -> None:
        from AdminToolkit.interface.disk.lvm import LVM
        lvm = LVM()
        RULE = '-'*50
        for vg in lvm.vgs:
            self.print()
            self.print(RULE)
            self.print(f"<red>VG</red> <blue>{vg.name}</blue>")
            self.print(f"  {vg.hsize} / {vg.hfree}")
            self.print(f"  {vg.number_of_extents:_} / {vg.number_of_free_extents:_} extents of {vg.extent_hsize}")
            _ = ' '.join([f"<green>{pv.name}</green>" for pv in vg.pvs])
            self.print(f"  PV: {_}")

            for lv in vg.lvs:
                self.print('  ' + '-'*10)
                self.print(f"  <red>LV</red> <blue>{lv.name}</blue>")
                layout = ' '.join(lv.layout)
                self.print(f"    {lv.hsize}   on {lv.number_of_segments} segments")
                self.print(f"    layout: {layout}")

        for pv in lvm.pvs:
            self.print()
            self.print(RULE)
            self.print(f"<red>PV</red> <blue>{pv.name}</blue> — <blue>{pv.vg_name}</blue>")
            self.print(f"  {pv.hsize} / {pv.hfree}")
            self.print(f"  {pv.number_of_extents:_} / {pv.number_of_free_extents:_} extents")
            start = 0

            def print_segment(start: int, end: int, name: str = None) -> None:
                size = end - start + 1
                if name is None:
                    name = "free segments"
                self.print(f"  {start:9_} - {end:9_} / {size:9_} : <blue>{name}</blue>")

            for sg in pv.segments:
                if sg.start != start:
                    end = sg.start - 1
                    self.print_segment(start, end)
                print_segment(sg.start, sg.end, sg.name)
                start = sg.end + 1
            if start != pv.number_of_extents:
                end = pv.number_of_extents - 1
                print_segment(start, end)
