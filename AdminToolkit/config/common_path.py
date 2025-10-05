####################################################################################################
#
# -
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from pathlib import Path

####################################################################################################

ROOT = Path('/')
DEV = Path('/dev')
ETC = Path('/etc')
PROC = Path('/proc')
SYS = Path('/sys')
RUN = Path('/run')
USR_BIN = Path('/usr/bin')

####################################################################################################

def cmd(name: str) -> Path:
    return USR_BIN.joinpath(name)

def proc(name: str) -> Path:
    return PROC.joinpath(name)

####################################################################################################

PROC_MOUNT = proc('self/mounts')
PROC_MDSTAT = proc('mdstat')

SYS_BLOCK = SYS.joinpath('block')
DEV_DISK = DEV.joinpath('disk')

SYSTEM_RELEASE_CPE = ETC.joinpath('system-release-cpe')
REDHAT_RELEASE = ETC.joinpath('redhat-release')

####################################################################################################

DD = cmd('dd')
DF = cmd('df')
DU = cmd('du')
IP = cmd('ip')
LOCATE = cmd('plocate')
LSBLK = cmd('lsblk')
MDADM = cmd('mdadm')
MOUNT = cmd('mount')
PARTED = cmd('parted')
PVDISPLAY = cmd('pvdisplay')
VGS = cmd('vgs')
