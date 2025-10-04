####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

__all__ = ['LVM']

####################################################################################################

from pathlib import Path
from pprint import pprint
from typing import Iterator

from AdminToolkit import common_path as cp
from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.tools.object import to_namedtuple
from AdminToolkit.tools.subprocess import run_command
from AdminToolkit.tools.format import byte_humanize

####################################################################################################

class LvmBase:

    ##############################################

    def __init__(self, data: 'PvInfo') -> None:
        self._data = data
        self._sg = []

    ##############################################

    def add_segment(self, sg: 'PvSegment') -> None:
        self._sg.append(sg) 

    @property
    def segments(self) -> Iterator['PvSegment']:
        return iter(sorted(self._sg, key=lambda _: _.start))

####################################################################################################

class PV(LvmBase):

    ##############################################

    def __init__(self, data: 'PvInfo') -> None:
        super().__init__(data)

    ##############################################

    @property
    def dev_path(self) -> Path:
        return Path(self._data.pv_name)

    @property
    def name(self) -> str:
        return self.dev_path.name

    @property
    def vg_name(self) -> str:
        return self._data.vg_name

    @property
    def number_of_extents(self) -> int:
        return self._data.pv_pe_count

    @property
    def number_of_free_extents(self) -> int:
        return self._data.pv_pe_count - self._data.pv_pe_alloc_count

    @property
    def size(self) -> int:
        return self._data.pv_size

    @property
    def free(self) -> int:
        return self._data.pv_free

    @property
    def hsize(self) -> int:
        return byte_humanize(self.size)

    @property
    def hfree(self) -> int:
        return byte_humanize(self.free)

####################################################################################################

class PvSegment:

    ##############################################

    def __init__(self, data: 'PvSegInfo') -> None:
        self._data = data

    ##############################################

    @property
    def pv_name(self) -> str:
        return self._data.pv_name

    @property
    def vg_name(self) -> str:
        return self._data.vg_name

    @property
    def name(self) -> str:
        return self._data.lv_name

    @property
    def lv_name(self) -> str:
        name = self._data.lv_name
        for pattern in ('_rmeta', '_rimage'):
            i = name.find(pattern)
            if i != -1:
                return name[1:i]
        return name

    @property
    def start(self) -> int:
        return self._data.pvseg_start

    @property
    def number_of_extents(self) -> int:
        return self._data.pvseg_size

    @property
    def end(self) -> int:
        return self.start + self.number_of_extents -1

####################################################################################################

class VG(LvmBase):

    ##############################################

    def __init__(self, data: 'VgInfo') -> None:
        super().__init__(data)
        self._pv = {}
        self._lv = {}

    ##############################################

    @property
    def name(self) -> str:
        return self._data.vg_name

    @property
    def extent_size(self) -> int:
        return self._data.vg_extent_size

    @property
    def extent_hsize(self) -> str:
        return byte_humanize(self.extent_size)

    @property
    def number_of_extents(self) -> int:
        return self._data.vg_extent_count

    @property
    def number_of_free_extents(self) -> int:
        return self._data.vg_free_count

    @property
    def size(self) -> int:
        return self._data.vg_size

    @property
    def free(self) -> int:
        return self._data.vg_free

    @property
    def hsize(self) -> int:
        return byte_humanize(self.size)

    @property
    def hfree(self) -> int:
        return byte_humanize(self.free)

    ##############################################

    def add_lv(self, lv: 'LV') -> None:
        self._lv[lv.name] = lv

    def add_pv(self, pv: PV) -> None:
        if pv.name not in self._pv:
            self._pv[pv.name] = pv

    @property
    def pvs(self) -> Iterator[PV]:
        return iter(sorted(self._pv.values(), key=lambda _: _.name))

    @property
    def lvs(self) -> Iterator['LV']:
        return iter(sorted(self._lv.values(), key=lambda _: _.name))

####################################################################################################

class LV(LvmBase):

    ##############################################

    def __init__(self, data: 'LvInfo') -> None:
        super().__init__(data)

    ##############################################

    @property
    def name(self) -> str:
        return self._data.lv_name

    # @property
    # def number_of_extents(self) -> int:
    #     return self._data.lv_

    @property
    def number_of_segments(self) -> int:
        return self._data.seg_count

    @property
    def size(self) -> int:
        return self._data.lv_size

    @property
    def hsize(self) -> int:
        return byte_humanize(self.size)

    @property
    def dev_path(self) -> Path:
        return Path(self._data.lv_path)

    @property
    def dev_dm_path(self) -> Path:
        return Path(self._data.lv_dm_path)

    @property
    def layout(self) -> str:
        return self._data.lv_layout

    @property
    def is_raid(self) -> bool:
        return 'raid' in self.layout

    @property
    def is_linear(self) -> bool:
        return 'linear' in self.layout

####################################################################################################

class LVM:

    ##############################################

    @classmethod
    def call_xvs(cls, name: str, segments: bool = False) -> list:
        XVS = cp.cmd(f'{name}s')
        raise_if_not_root(f'lvm {XVS} command')
        if name == 'pv' and segments:
            options = '--options=pvseg_all,pv_name,vg_name,lv_name'
            cls_name = 'PvSegInfo'
        else:
            options = f'--options={name}_all,vg_name'
            cls_name = f'{name.capitalize()}Info'
        cmd = (
            XVS,
            '--units=b',
            '--nosuffix',
            options,
            '--reportformat=json_std',
        )
        _ = run_command(cmd, to_json=True)
        data = _['report'][0][name]
        return [to_namedtuple(cls_name, _) for _ in data]

    ##############################################

    def __init__(self) -> None:
        self.pv = {_.name: _ for _ in map(PV, self.call_xvs('pv'))}
        self.vg = {_.name: _ for _ in map(VG, self.call_xvs('vg'))}
        self.lv = {_.name: _ for _ in map(LV, self.call_xvs('lv'))}
        for sg in map(PvSegment, self.call_xvs('pv', segments=True)):
            if sg.lv_name:
                pv = self.pv[Path(sg.pv_name).name]
                vg = self.vg[sg.vg_name]
                lv = self.lv[sg.lv_name]
                sg.pv = pv
                sg.vg = vg
                sg.lv = lv
                lv.vg = vg
                pv.add_segment(sg)
                vg.add_segment(sg)
                lv.add_segment(sg)
                vg.add_pv(pv)
                vg.add_lv(lv)

    ##############################################

    @property
    def pvs(self) -> Iterator[PV]:
        return iter(sorted(self.pv.values(), key=lambda _: _.name))

    @property
    def vgs(self) -> Iterator[VG]:
        return iter(sorted(self.vg.values(), key=lambda _: _.name))

####################################################################################################


if __name__ == '__main__':
    for type_ in ('pv', 'vg', 'lv'):
        print('-'*10)
        _ = LVM.call_xvs(type_)
        pprint(_)
    _ = LVM.call_xvs('pv', segments=True)
    pprint(_)

    lvm = LVM()
    for vg in lvm.vgs:
        print()
        print('-'*50)
        print(f"VG {vg.name}")
        print(f"{vg.number_of_extents:_} / {vg.number_of_free_extents:_} extents of {vg.extent_hsize}")
        print(f"{vg.hsize} / {vg.hfree}")
        print([pv.name for pv in vg.pvs])

        for lv in vg.lvs:
            print('-'*10)
            print(f"LV {lv.name} {lv.layout}")
            print(f"{lv.hsize}   on {lv.number_of_segments} segments")

    for pv in lvm.pvs:
        print()
        print('-'*50)
        print(f"PV {pv.name} / {pv.vg_name}")
        print(f"{pv.number_of_extents:9_} / {pv.number_of_free_extents:_} extents")
        print(f"{pv.hsize} / {pv.hfree}")
        start = 0

        def print_segment(start: int, end: int, name: str = None) -> None:
            size = end - start + 1
            if name is None:
                name = "free segments"
            print(f"{start:9_} — {end:9_} / {size:9_} : {name}")

        for sg in pv.segments:
            if sg.start != start:
                end = sg.start - 1
                print_segment(start, end)
            print_segment(sg.start, sg.end, sg.name)
            start = sg.end + 1
        if start != pv.number_of_extents:
            end = pv.number_of_extents - 1
            print_segment(start, end)
