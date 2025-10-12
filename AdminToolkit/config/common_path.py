####################################################################################################
#
# -
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from pathlib import Path

from AdminToolkit.tools.mockup import MOCKUP_CACHE

####################################################################################################

class MockupPath(Path):

    ##############################################

    def read_text(self) -> str:
        return MOCKUP_CACHE.read_text(self)

####################################################################################################

ROOT = Path('/')
DEV = Path('/dev')
ETC = Path('/etc')
PROC = MockupPath('/proc')
SYS = Path('/sys')
RUN = Path('/run')
USR_BIN = Path('/usr/bin')
USR_SBIN = Path('/usr/sbin')

####################################################################################################

SYSTEM_RELEASE_CPE = ETC.joinpath('system-release-cpe')
REDHAT_RELEASE = ETC.joinpath('redhat-release')
DEBIAN_VERSION = ETC.joinpath('debian_version')

IS_DEBIAN = DEBIAN_VERSION.exists()

####################################################################################################

def cmd(name: str) -> Path:
    return USR_BIN.joinpath(name)

def scmd(name: str) -> Path:
    # _ = USR_BIN.joinpath(name)
    # if _.exists():
    #    return _
    # else:
    #     return USR_SBIN.joinpath(name)
    if IS_DEBIAN:
        return USR_SBIN.joinpath(name)
    else:
        return USR_BIN.joinpath(name)

def proc(name: str) -> Path:
    return PROC.joinpath(name)

####################################################################################################

PROC_CPUINFO = proc('cpuinfo')
PROC_MOUNT = proc('self/mounts')
PROC_MDSTAT = proc('mdstat')

SYS_BLOCK = SYS.joinpath('block')
DEV_DISK = DEV.joinpath('disk')

####################################################################################################

DD = cmd('dd')
DUMPE2FS = scmd('dumpe2fs')
DF = cmd('df')
DU = cmd('du')
IP = scmd('ip')
LOCATE = cmd('plocate')
LSBLK = cmd('lsblk')
MDADM = scmd('mdadm')
MOUNT = cmd('mount')
PARTED = scmd('parted')
PVDISPLAY = scmd('pvdisplay')
UMOUNT = cmd('umount')
VGS = scmd('vgs')
