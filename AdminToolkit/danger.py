####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

__all__ = ['AbortAction', 'raise_if_root_device', 'CONFIRM_DANGER']

####################################################################################################

from pathlib import Path
import os
import random

from AdminToolkit.interface.disk.mount import get_root_device
# from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.printer import atprint

####################################################################################################

LINESEP = os.linesep

####################################################################################################

class AbortAction(NameError):
    pass

class IsRootAbortAction(AbortAction):
    pass

####################################################################################################

def raise_if_root_device(name: str | Path):
    from AdminToolkit.interface.disk.partition import partion_to_device
    root_device = str(get_root_device())
    path = Path(name)
    if not path.exists():
        raise AbortAction(f"Device {name} doesn't exists")
    # resolve /dev/disk/... /dev/mapper/...
    if path.is_symlink():
        name = str(path.resolve())
    name = str(partion_to_device(name))
    atprint(f"Resolved to <blue>{name}</blue>")
    if root_device == name:
        raise IsRootAbortAction(f'Device {name} is root device')

####################################################################################################

def CONFIRM_DANGER(message: str):
    # , printer=None
    _ = str(random.random()*1000_000)
    _ = _[1] + _[3] + _[5]
    CONFIRMATION = f'YES{_}!'
    # if printer is not None:
    #     printer(CONFIRMATION)
    #     prompt = ''
    # else:
    #     prompt = message + f' (confirm with: "{CONFIRMATION}"): '
    # rc = input(prompt)
    prompt = '<red>' + message + '</red>' + LINESEP + f'  (confirm with: "<green>{CONFIRMATION}</green>"): '
    atprint(prompt)
    rc = input()
    if rc != CONFIRMATION:
        raise AbortAction

####################################################################################################


if __name__ == '__main__':
    CONFIRM_DANGER('Test...')
