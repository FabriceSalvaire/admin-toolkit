####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['System']

####################################################################################################

from AdminToolkit.cli import CommandGroup
from AdminToolkit.interface.system import System
from AdminToolkit.interface.network import Network

####################################################################################################

class SystemCommands(CommandGroup):

    ##############################################

    def system(self) -> None:
        _ = System()
        self.print(f"OS: {_.os_product.capitalize()} {_.os_version}")
        self.print(f"Kernel: {_.kernel}")

    ##############################################

    def network(self) -> None:
        _ = System()
        self.print(f"Host: <blue>{_.hostname}</blue>")
        self.print()
        network = Network()
        for _ in sorted(network, key=lambda _: _.name):
            up = '<green> UP </green>' if _.is_up else '<red>DOWN</red>'
            if _.is_unknown:
                up = '<orange> ?  </orange>'
            ipv4 = _.ipv4 if _.ipv4 else ''
            ipv6 = _.ipv6 if _.ipv6 else ''
            self.print(f"<blue>{_.name:10}</blue> {up} {ipv4:16} {ipv6}")
