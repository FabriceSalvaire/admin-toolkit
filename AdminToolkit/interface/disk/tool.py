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

# from AdminToolkit.tools.printer import atprint

type PathStr = Path | str

####################################################################################################

def to_dev_path(dev_path: PathStr, resolve: bool = False) -> Path:
    """Return a `Path` instance corresponding to the path of a device.
    The argument `dev_path` can be a device name, a link path or a device path.
    It checks the device exists.
    A link path is resolved to its cannonical path if `resolved` is set.
    """
    if isinstance(dev_path, str):
        if dev_path.startswith('sd'):
            dev_path = Path('/dev').joinpath(dev_path)
    dev_path = Path(dev_path)
    if not dev_path.exists():
        raise NameError(f"Device path {dev_path} doesn't exists")
    if resolve:
        resolved_path = dev_path.resolve()
        # atprint(f"Resolved to <blue>{resolved_path}</blue>")
        return resolved_path
    else:
        return dev_path

####################################################################################################

def is_sd(name: str) -> bool:
    """Return `True` if name mathches `sd<number>`"""
    return name.startswith('sd') and len(name) == 3 and name[2].isnumeric()
