# https://discuss.python.org/t/disk-space-used-by-a-file/45205/3

from pathlib import Path
from pprint import pprint
import os

file = Path(__file__).parent
print(file)

pprint(os.statvfs(file))
# os.statvfs_result(f_bsize=4096, f_frsize=4096, f_blocks=110672266, f_bfree=5704149, f_bavail=137365, f_files=28180480, f_ffree=24794366, f_favail=24794366, f_flag=4096, f_namemax=255)

pprint(os.stat(file))

_  = file.stat()
pprint(_)
# os.stat_result(st_mode=33204, st_ino=1320513, st_dev=64515, st_nlink=1, st_uid=1000, st_gid=1000, st_size=129, st_atime=1759584439, st_mtime=1759584439, st_ctime=1759584439)
# pprint(dir(_))
print('size', _.st_size)
print('fs block size', _.st_blksize)
print('blocks', _.st_blocks)
print('size on disk', _.st_blocks * 512)
print('link', _.st_nlink)
