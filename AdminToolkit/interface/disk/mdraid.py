####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from pathlib import Path
from dataclasses import dataclass

from AdminToolkit.config import common_path as cp
from AdminToolkit.common.subprocess import iter_on_command_output

####################################################################################################

@dataclass
class MdRaidDevice:
    """Class to store the properties of a MDRaid device"""

    number_name: str
    status: str
    raid_type: str
    devices: dict

    name: str = None
    uuid: str = None

    ##############################################

    @property
    def dev_path_number(self) -> Path:
        return cp.DEV.joinpath(self.number_name)

####################################################################################################

class MdRaidDevices:

    """Class to query MDRaid devices"""

    ##############################################

    def __init__(self):
        self._raid_types = ()
        self._devices = self.proc_mdstat()
        for _ in self._devices:
            self.mdadm_detail(_)

    ##############################################

    def __iter__(self) -> MdRaidDevice:
        return iter(self._devices)

    @property
    def raid_types(self) -> [str]:
        """Return the types of RAID supported by the kernel"""
        return tuple(self._raid_types)

    ##############################################

    def proc_mdstat(self) -> list[MdRaidDevice]:
        """Read information from `/proc/mdstat` and return a list of `MdRaidDevice` instances"""
        content = cp.PROC_MDSTAT.read_text()
        mdraid_devices = []
        for line in content.splitlines():
            # print(line)
            if line.startswith('Personalities : '):
                self._raid_types = [_.replace('[', '').replace(']', '') for _ in line.split() if _.startswith('[')]
                # print(personalities)
            elif line.startswith('md'):
                if not self._raid_types:
                    raise NameError('personalities are not defined')
                name, status, *right = [_ for _ in line.split() if _ != ':']
                if right[0].startswith('('):
                    # (auto-read-only)
                    right.pop(0)
                raid_type = right.pop(0)
                if raid_type not in self._raid_types:
                    raise NameError('unknown raid type: {raid_type}')
                devices = {}
                for part in right:
                    i = part.find('[')
                    if i == -1:
                        raise NameError('device name error: {part}')
                    device = part[:i]
                    index = int(part[i+1:-1])
                    # print(device, index)
                    if not device.startswith('sd'):
                        raise NameError('device is not sd: {part}')
                    devices[index] = device
                # print(name, status, raid_type, devices)
                mdraid_device = MdRaidDevice(
                    number_name=name,
                    status=status,
                    raid_type=raid_type,
                    devices=devices,
                )
                mdraid_devices.append(mdraid_device)
        return mdraid_devices

    ##############################################

    def mdadm_detail(self, md_device: MdRaidDevice) -> None:
        """Call `mdadm` to get additional information"""
        cmd = (
            cp.MDADM,
            '--detail',
            '--export',
            str(md_device.dev_path_number),
        )
        for line in iter_on_command_output(cmd):
            key, value = line.split('=')
            match key:
                case 'MD_UUID':
                    md_device.uuid = value
                case 'MD_DEVNAME':
                    md_device.name = value


####################################################################################################

if __name__ == '__main__':
    from AdminToolkit.config import config
    config.MOCKUP = True
    config.DEBUG = True
    for _ in MdRaidDevices():
        print(_)
