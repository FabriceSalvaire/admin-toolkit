####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['to_dev_path', 'is_sd']

####################################################################################################

from pathlib import Path

from AdminToolkit.printer import atprint

####################################################################################################

def to_dev_path(dev_path: str | Path, resolve: bool = False) -> Path:
    if isinstance(dev_path, str):
        if dev_path.startswith('sd'):
            dev_path = Path('/dev').joinpath(dev_path)
    dev_path = Path(dev_path)
    if not Path(dev_path).exists():
        raise NameError(f"Device path {dev_path} doesn't exists")
    if resolve:
        resolved_path = dev_path.resolve()
        # atprint(f"Resolved to <blue>{resolved_path}</blue>")
        return resolved_path
    else:
        return dev_path

####################################################################################################

def is_sd(name: str) -> bool:
    return name.startswith('sd') and len(name) == 3
