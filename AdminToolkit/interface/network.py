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
from typing import Iterator

from AdminToolkit.config import common_path as cp
from AdminToolkit.tools.object import namedtuple_factory
from AdminToolkit.tools.subprocess import run_command

####################################################################################################

InterfaceInfo = namedtuple_factory(
    'InterfaceInfo',
    (
        'addr_info',
        'address',
        'altnames',
        'broadcast',
        'flags',
        'group',
        'ifindex',
        'ifname',
        'link_type',
        'mtu',
        'operstate',
        'permaddr',
        'qdisc',
        'txqlen',
    ),
)

AddressInfo = namedtuple_factory(
    'AddressInfo',
    (
        'address',
        'broadcast',
        'dynamic',
        'family',
        'label',
        'local',
        'noprefixroute',
        'preferred_life_time',
        'prefixlen',
        'protocol',
        'scope',
        'stable_privacy',
        'valid_life_time',
    ),
)

####################################################################################################

class Interface:

    ##############################################

    def __init__(self, data: AddressInfo) -> None:
        self._data = data

    ##############################################

    @property
    def name(self) -> str:
        return self._data.ifname

    @property
    def is_down(self) -> bool:
        return 'DOWN' in self._data.operstate

    @property
    def is_unknown(self) -> bool:
        return 'UNKNOWN' in self._data.operstate

    @property
    def is_up(self) -> bool:
        return 'UP' in self._data.operstate

    @property
    def ipv4(self) -> bool:
        for _ in self._data.addr_info:
            if _.family == 'inet':
                return _.local
        return None

    @property
    def ipv6(self) -> bool:
        for _ in self._data.addr_info:
            if _.family == 'inet6':
                return _.local
        return None

####################################################################################################

class Network:

    ##############################################

    def __init__(self) -> None:
        self._interfaces = {}
        self._ip_addr()

    ##############################################

    def _ip_addr(self) -> None:
        cmd = (
            cp.IP,
            '-json',
            'addr',
        )
        data = run_command(cmd, to_json=True)
        for interface in data:
            # print()
            # pprint(interface)
            if 'addr_info' in interface:
                interface['addr_info'] = [AddressInfo(**_) for _ in interface['addr_info']]
            # _ = to_namedtuple('InterfaceInfo', interface)
            _ = InterfaceInfo(**interface)
            _ = Interface(_)
            self._interfaces[_.name] = _

    ##############################################

    def __iter__(self) -> Iterator[Interface]:
        return iter(self._interfaces.values())

####################################################################################################


if __name__ == '__main__':
    network = Network()
    for _ in network:
        print(_.name, _.is_up, _.ipv4, _.ipv6)
