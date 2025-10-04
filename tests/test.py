####################################################################################################

import sys

from pprint import pprint

from AdminToolkit.interface.device import *
from AdminToolkit.interface.user import *

####################################################################################################

# print(is_root())
# sys.exit()

# _ = lsblk('sda')
# pprint(sorted(_.keys()))
# pprint(_)
# sys.exit()
# pprint(lsblk('sda1'))

# _ = parted('sda')
# pprint(_)
# last_end = 0
# for p in sorted(_.partitions, key=lambda p:p.start):
#     if last_end and p.start != last_end + 1:
#         gap = p.start - last_end
#         print(f'  Gap {gap:_}s {hsize(gap*512)}')
#     size = hsize(p.size*512)
#     print(f'{p.number:3} {p.start:16_} {p.end:16_} {size:16} {p.filesystem:16} {p.name}')
#     last_end = p.end
# sys.exit()

_ = BlockDevice('sda')
print('name', _.name)
print('size', _.hsize)
print('model', _.model)
print('removable', _.removable)
print('part table type', _.part_table_type)
# print(_.vendor)

for p in _.partitions:
    print('-'*10)
    print('name', p.name)
    print('part #', p.part_number, p.id)
    print('  type', p.part_type)
    print('  label', p.part_label)
    print('  flags', p.part_flags)
    print('size', p.size, p.hsize)
    print('type', p.type)
    print('mount', p.mountpoint, p.mountpoints)
    print('ro', p.ro)
    print('fs type', p.fs_type)
    print('  size', p.fs_size, p.fs_hsize)
    print('  used', p.fs_used, p.fs_hused)
    print('  %', p.fs_pused)
    print('gpt uuid', p.gpt_uuid)
    print('  start:end', p.gpt_start, p.gpt_end)
    print('  size', p.gpt_size, p.gpt_hsize)
    print('  flags', p.gpt_flags)
    print('  links', p.links)
