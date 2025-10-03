####################################################################################################

from pprint import pprint

from AdminToolkit.tools.mockup import MOCKUP_CACHE
from AdminToolkit.interface.disk.mdraid import *

####################################################################################################

MOCKUP_CACHE.add_file_mockup(
    PROC_MDSTAT,
    '''
Personalities : [raid1] [raid6] [raid5] [raid4] [linear] [multipath] [raid0] [raid10]
md127 : active (auto-read-only) raid1 sdc5[0] sdd5[1]
1936781312 blocks super 1.2 [2/2] [UU]
bitmap: 0/15 pages [0KB], 65536KB chunk

unused devices: <none
'''.strip())

MOCKUP_CACHE.add_cmd_mockup(
    (MDADM, '--detail', '--export', '/dev/md127'),
    '''
MD_LEVEL=raid1
MD_DEVICES=2
MD_METADATA=1.2
MD_UUID=d0d68537:3bc9e8fd:770d7d5e:353ce578
MD_DEVNAME=raid_2tb
MD_NAME=osiris:raid_2tb
MD_DEVICE_dev_sdd5_ROLE=1
MD_DEVICE_dev_sdd5_DEV=/dev/sdd5
MD_DEVICE_dev_sdc5_ROLE=0
MD_DEVICE_dev_sdc5_DEV=/dev/sdc5
'''.strip(),
    ''
)

####################################################################################################

#pprint(MOCKUP_CACHE._cache)

for _ in MdRaidDevices():
    pprint(_)
