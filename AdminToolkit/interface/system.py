####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = []

####################################################################################################

# from pprint import pprint
import os
# import socket

from AdminToolkit.config import common_path as cp

####################################################################################################

class System:

    ##############################################

    def __init__(self) -> None:
        _ = os.uname()
        # _.sysname = Linux
        self.hostname = _.nodename    # socket.gethostname()
        self.kernel = _.release
        # _.version
        self.machine = _.machine

        self._read_cpe()

    ##############################################

    def _read_cpe(self) -> None:
        # https://en.wikipedia.org/wiki/Common_Platform_Enumeration
        # cpe:<cpe_version>:<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>
        # part = /o for Operating Systems

        self.os_vendor = None
        self.os_product = None
        self.os_version = None
        if cp.SYSTEM_RELEASE_CPE.exists():
            data = cp.SYSTEM_RELEASE_CPE.read_text()
            parts = data.strip().split(':')
            # cpe:/o:fedoraproject:fedora:42
            if parts[1] != '/o':
                raise ValueError
            self.os_vendor, self.os_product, self.os_version = parts[2:5]
        elif cp.REDHAT_RELEASE.exists():
            # Fixme: cpe is far better...
            data = cp.REDHAT_RELEASE.read_text()
            # Fedora release 42 (Adams)
            self.os_product = data.split()[0]
            self.os_version = data
        elif cp.DEBIAN_VERSION.exists():
            self.os_vendor = 'Debian'
            self.os_product = 'Debian'
            self.os_version = cp.DEBIAN_VERSION.read_text().strip()

####################################################################################################


if __name__ == '__main__':
    _ = System()
    print(_.kernel)
    print(_.os_version)
