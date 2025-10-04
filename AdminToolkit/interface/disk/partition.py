####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['partion_to_device']

####################################################################################################

from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import struct
import uuid

from AdminToolkit import common_path as cp
from AdminToolkit.danger import raise_if_root_device   # , CONFIRM_DANGER
from AdminToolkit.interface.disk.tool import to_dev_path
from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.tools.object import fix_dict_key
from AdminToolkit.tools.subprocess import run_command, RUN_DANGEROUS

####################################################################################################

def partion_to_device(name: str) -> str:
    """Return sda for .../sda[0...9]"""
    name = str(name)
    if not name:
        raise ValueError
    i = len(name) - 1
    while i >= 0 and name[i].isnumeric():
        i -= 1
    _ = name[:i+1]
    _ = Path(_).name
    # print(name, _)
    return _

####################################################################################################

def fix_s_unit(d: dict) -> None:
    for key in ('start', 'end', 'size'):
        if key in d:
            _ = int(d[key][:-1])
            assert(d[key] == f'{_}s')
            d[key] = _

####################################################################################################

@dataclass
class GptPartion:
    end: int = None
    filesystem: str = None
    flags: str = None
    name: str = None
    number: int = None
    size: int = None
    start: int = None
    type: str = None
    # For GPT
    type_uuid: str = None
    uuid: str = None
    # for MsDOS
    type_id: str = None

####################################################################################################

@dataclass
class GptTable:
    label: str = None
    logical_sector_size: int = None
    max_partitions: str = None
    model: str = None
    partitions: str = None
    path: str = None
    physical_sector_size: str = None
    size: int = None
    transport: str = None
    uuid: str = None

####################################################################################################

def parted(dev_path: str | Path) -> dict:
    raise_if_not_root(cp.PARTED)
    dev_path = to_dev_path(dev_path)
    cmd = (
        cp.PARTED,
        '--json',
        str(dev_path),
        'unit s',
        'print'
    )
    data = run_command(cmd, to_json=True)
    data = data['disk']
    # pprint(data)
    new_partitions = []
    for part in data['partitions']:
        fix_dict_key(part)
        fix_s_unit(part)
        for key in ('filesystem', 'name'):
            if key not in part or part[key] is None:
                part[key] = ''
        # pprint(part)
        part = GptPartion(**part)
        new_partitions.append(part)
    data['partitions'] = new_partitions
    fix_s_unit(data)
    data = GptTable(**fix_dict_key(data))
    return data

####################################################################################################

# See http://en.wikipedia.org/wiki/GUID_Partition_Table

GPT_HEADER_FORMAT = '''
8s  signature
4s  revision
L   header_size
L   crc32
4x  _
Q   current_lba
Q   backup_lba
Q   first_usable_lba
Q   last_usable_lba
16s disk_guid
Q   part_entry_start_lba
L   num_part_entries
L   part_entry_size
L   crc32_part_array
'''

GPT_PARTITION_FORMAT = '''
16s type_uuid
16s uuid
Q   start
Q   end
Q   flags
72s name
'''

####################################################################################################

def _make_format(name: str, format: str, extras: list = []):   # -> list[str, ]
    type_and_name = [_.split(None, 1) for _ in format.strip().splitlines()]
    # print(type_and_name)
    fmt = ''.join(t for t, n in type_and_name)
    fmt = '<'+fmt
    # print(fmt)
    _ = [n for t, n in type_and_name if n != '_'] + extras
    tupletype = namedtuple(name, _)
    # pprint(tupletype)
    return (fmt, tupletype)

####################################################################################################

def _to_uuid(value: bytes) -> str:
    return str(uuid.UUID(bytes_le=value))

####################################################################################################

def read_device(dev_path: str | Path, count: int = 1024) -> bytes:
    raise_if_not_root(cp.DD)
    dev_path = to_dev_path(dev_path)
    cmd = (
        cp.DD,
        f'count={count}',
        f'if={dev_path}',
    )
    return run_command(cmd, to_bytes=True)

####################################################################################################

def clear_device(dev_path: str | Path, count: int = 1) -> bytes:
    # !!! DANGER !!!
    raise_if_not_root(cp.DD)
    dev_path = to_dev_path(dev_path)
    raise_if_root_device(dev_path)
    cmd = (
        cp.DD,
        f'count={count}',
        f'if=/dev/zero',
        f'of={dev_path}',
    )
    return RUN_DANGEROUS(f"Clear device {dev_path}", cmd, print_output=True)

####################################################################################################

class GptError(Exception):
    pass

####################################################################################################

def read_header(stream: bytes, lba_size: int = 512):
    fmt, GPTHeader = _make_format('GptTableRaw', GPT_HEADER_FORMAT)
    header_size = struct.calcsize(fmt)
    mbr_size = 1 * lba_size
    # skip MBR
    # fp.seek(mbr_size)
    # data = fp.read(header_size)
    data = stream[mbr_size:mbr_size+header_size]
    # pprint(data)
    header = GPTHeader._make(struct.unpack(fmt, data))
    if header.signature != b'EFI PART':
        raise GptError(f'Bad signature: {header.signature}')
    if header.revision != b'\x00\x00\x01\x00':
        raise GptError(f'Bad revision: {header.revision}')
    if header.header_size < 92:
        raise GptError(f'Bad header size: {header.header_size}')
    # TODO check crc32
    #   use zlib.crc32
    header = header._replace(
        disk_guid=_to_uuid(header.disk_guid),
    )
    return header

####################################################################################################

def read_partitions(stream: bytes, header, lba_size: int = 512):
    fmt, GPTPartition = _make_format('GptPartitionRaw', GPT_PARTITION_FORMAT, extras=['number'])
    # fp.seek(header.part_entry_start_lba * lba_size)
    index = header.part_entry_start_lba * lba_size
    for part_number in range(1, 1+header.num_part_entries):
        # data = fp.read(header.part_entry_size)
        next_index = index + header.part_entry_size
        data = stream[index:next_index]
        index = next_index
        if len(data) < struct.calcsize(fmt):
            raise GptError('Short partition entry')
        part = GPTPartition._make(struct.unpack(fmt, data) + (part_number,))
        # skip unused entries
        if part.type_uuid == 16*b'\x00':
            continue
        part = part._replace(
            type_uuid=_to_uuid(part.type_uuid),
            uuid=_to_uuid(part.uuid),
            # do C-style string termination; otherwise you'll see a long row of NILs for most names
            name=part.name.decode('utf-16').split('\0', 1)[0],
        )
        yield part

####################################################################################################


if __name__ == '__main__':
    from AdminToolkit.tools.format import byte_humanize

    dev_name = 'sda'
    # dev_name = 'sdc'

    try:
        stream = read_device(dev_name)
        # pprint(stream)
        header = read_header(stream)
        pprint(header)
        for part in read_partitions(stream, header):
            pprint(part)
    except GptError:
        pass

    print()
    _ = parted(dev_name)
    pprint(_)
    print()
    last_end = 0
    for p in sorted(_.partitions, key=lambda p: p.start):
        if last_end and p.start != last_end + 1:
            gap = p.start - last_end
            print(f'  Gap {gap:_}s {byte_humanize(gap*512)}')
        size = byte_humanize(p.size*512)
        print(f'{p.number:3} {p.start:16_} {p.end:16_} {size:16} {p.filesystem:16} {p.name}')
        last_end = p.end
