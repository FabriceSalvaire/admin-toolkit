####################################################################################################

from pprint import pprint

from AdminToolkit.tools.mockup import MOCKUP_CACHE
from AdminToolkit.interface.disk.lvm import *

####################################################################################################

MOCKUP_CACHE.add_cmd_mockup(
    ('/usr/bin/pvs', '--units=b', '--nosuffix', '--options=pv_all,vg_name', '--reportformat=json_std'),
    '''
{
"report": [{
"pv": [
{"pv_fmt":"lvm2", "pv_uuid":"skHRvY-otct-axSM-Ggyp-g7sX-sRSL-lXLDV6", "dev_size":"3873562624", "pv_name":"/dev/md127", "pv_major":"9", "pv_minor":"127", "pv_mda_free":"1014", "pv_mda_size":"2040", "pv_ext_vsn":"2", "pe_start":"2048", "pv_size":"3873554432", "pv_free":"727908352", "pv_used":"3145646080", "pv_attr":"a--", "pv_allocatable":"allocatable", "pv_exported":"", "pv_missing":"", "pv_pe_count":"472846", "pv_pe_alloc_count":"383990", "pv_tags":"", "pv_mda_count":"1", "pv_mda_used_count":"1", "pv_ba_start":"0", "pv_ba_size":"0", "pv_in_use":"used", "pv_duplicate":"", "pv_device_id":"", "pv_device_id_type":"", "vg_name":"vg_raid_2tb"},
{"pv_fmt":"lvm2", "pv_uuid":"1pMg5P-ivjH-kHPk-Yhcc-YLF1-jbCr-LlR6WB", "dev_size":"1951418368", "pv_name":"/dev/sda3", "pv_major":"8", "pv_minor":"3", "pv_mda_free":"1005", "pv_mda_size":"2040", "pv_ext_vsn":"2", "pe_start":"2048", "pv_size":"1951399936", "pv_free":"884408320", "pv_used":"1066991616", "pv_attr":"a--", "pv_allocatable":"allocatable","pv_exported":"", "pv_missing":"", "pv_pe_count":"29776", "pv_pe_alloc_count":"16281", "pv_tags":"", "pv_mda_count":"1", "pv_mda_used_count":"1", "pv_ba_start":"0", "pv_ba_size":"0", "pv_in_use":"used", "pv_duplicate":"", "pv_device_id":"", "pv_device_id_type":"", "vg_name":"vg_raid_1tb"},
{"pv_fmt":"lvm2", "pv_uuid":"1xqsxY-38KH-Ze7l-Ikw5-3UbM-RUv3-dQA5mO", "dev_size":"1951425968", "pv_name":"/dev/sdb3", "pv_major":"8", "pv_minor":"19", "pv_mda_free":"1005", "pv_mda_size":"2040", "pv_ext_vsn":"2", "pe_start":"2048", "pv_size":"1951399936", "pv_free":"1031208960", "pv_used":"920190976", "pv_attr":"a--", "pv_allocatable":"allocatable", "pv_exported":"", "pv_missing":"", "pv_pe_count":"29776", "pv_pe_alloc_count":"14041", "pv_tags":"", "pv_mda_count":"1", "pv_mda_used_count":"1", "pv_ba_start":"0", "pv_ba_size":"0", "pv_in_use":"used", "pv_duplicate":"", "pv_device_id":"", "pv_device_id_type":"", "vg_name":"vg_raid_1tb"}
]}]}
'''.strip(),
    ''
)

# > pvscan
# PV /dev/md127   VG vg_raid_2tb     lvm2 [1,80 TiB / 347,09 GiB free]
# PV /dev/sda3    VG vg_raid_1tb     lvm2 [930,50 GiB / <421,72 GiB free]
# PV /dev/sdb3    VG vg_raid_1tb     lvm2 [930,50 GiB / <491,72 GiB free]
# Total: 3 [3,62 TiB] / in use: 3 [3,62 TiB] / in no VG: 0 [0   ]

# > pvs
# PV         VG          Fmt  Attr PSize   PFree
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g

# _ = call_xvs('pv')
# pprint(_)

####################################################################################################

# > pvs --segment
# PV         VG          Fmt  Attr PSize   PFree    Start  SSize
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g      0   8182
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g   8182 281600
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g 289782    512
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g 290294  89600
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g 379894   4096
# /dev/md127 vg_raid_2tb lvm2 a--    1,80t  347,09g 383990  88856
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g      0    256
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g    256     64
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g    320      1
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g    321    575
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g    896   1430
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g   2326      1
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g   2327  11200
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g  13527      1
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g  13528   1408
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g  14936   1920
# /dev/sda3  vg_raid_1tb lvm2 a--  930,50g <421,72g  16856  12920
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g      0      1
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g      1   1430
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g   1431      1
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g   1432  11200
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g  12632      1
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g  12633   1408
# /dev/sdb3  vg_raid_1tb lvm2 a--  930,50g <491,72g  14041  15735

MOCKUP_CACHE.add_cmd_mockup(
    ('/usr/bin/pvs', '--units=b', '--nosuffix', '--options=pvseg_all,pv_name,vg_name,lv_name', '--reportformat=json_std'),
    '''
{
"report": [
{
"pv": [
{"pvseg_start":"0", "pvseg_size":"8182", "pv_name":"/dev/md127", "vg_name":"vg_raid_2tb", "lv_name":"root_fc21"},
{"pvseg_start":"8182", "pvseg_size":"281600", "pv_name":"/dev/md127", "vg_name":"vg_raid_2tb", "lv_name":"backup_2tb"},
{"pvseg_start":"289782", "pvseg_size":"512", "pv_name":"/dev/md127", "vg_name":"vg_raid_2tb", "lv_name":"root_fc21"},
{"pvseg_start":"290294", "pvseg_size":"89600", "pv_name":"/dev/md127", "vg_name":"vg_raid_2tb", "lv_name":"isis_backup"},
{"pvseg_start":"379894", "pvseg_size":"4096", "pv_name":"/dev/md127", "vg_name":"vg_raid_2tb", "lv_name":"ntfs_disk1"},
{"pvseg_start":"383990", "pvseg_size":"88856", "pv_name":"/dev/md127", "vg_name":"vg_raid_2tb", "lv_name":""},
{"pvseg_start":"0", "pvseg_size":"256", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"swap_0"},
{"pvseg_start":"256", "pvseg_size":"64", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"tmp_0"},
{"pvseg_start":"320", "pvseg_size":"1", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_rmeta_0]"},
{"pvseg_start":"321", "pvseg_size":"575", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":""},
{"pvseg_start":"896", "pvseg_size":"1430", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_rimage_0]"},
{"pvseg_start":"2326", "pvseg_size":"1", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"[backup_1tb_rmeta_0]"},
{"pvseg_start":"2327", "pvseg_size":"11200", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"[backup_1tb_rimage_0]"},
{"pvseg_start":"13527", "pvseg_size":"1", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_12_rmeta_0]"},
{"pvseg_start":"13528", "pvseg_size":"1408", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_12_rimage_0]"},
{"pvseg_start":"14936", "pvseg_size":"1920", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":"ntfs_disk2"},
{"pvseg_start":"16856", "pvseg_size":"12920", "pv_name":"/dev/sda3", "vg_name":"vg_raid_1tb", "lv_name":""},
{"pvseg_start":"0", "pvseg_size":"1", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_rmeta_1]"},
{"pvseg_start":"1", "pvseg_size":"1430", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_rimage_1]"},
{"pvseg_start":"1431", "pvseg_size":"1", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":"[backup_1tb_rmeta_1]"},
{"pvseg_start":"1432", "pvseg_size":"11200", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":"[backup_1tb_rimage_1]"},
{"pvseg_start":"12632", "pvseg_size":"1", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_12_rmeta_1]"},
{"pvseg_start":"12633", "pvseg_size":"1408", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":"[root_debian_12_rimage_1]"},
{"pvseg_start":"14041", "pvseg_size":"15735", "pv_name":"/dev/sdb3", "vg_name":"vg_raid_1tb", "lv_name":""}
]}]}
'''.strip(),
    ''
)

# _ = call_xvs('pv', segments=True)
# pprint(_)

####################################################################################################

MOCKUP_CACHE.add_cmd_mockup(
    ('/usr/bin/vgs', '--units=b', '--nosuffix', '--options=vg_all,vg_name', '--reportformat=json_std'),
    '''
{
"report": [{
"vg": [
{"vg_fmt":"lvm2", "vg_uuid":"MIe72w-ugVh-lF0m-kUzX-h7OQ-60tH-3i8JoP", "vg_name":"vg_raid_1tb", "vg_attr":"wz--n-", "vg_permissions":"writeable", "vg_extendable":"extendable", "vg_exported":"", "vg_autoactivation":"enabled", "vg_partial":"", "vg_allocation_policy":"normal", "vg_clustered":"", "vg_shared":"", "vg_size":"3902799872", "vg_free":"1915617280", "vg_sysid":"", "vg_systemid":"", "vg_lock_type":"", "vg_lock_args":"", "vg_extent_size":"65536", "vg_extent_count":"59552", "vg_free_count":"29230", "max_lv":"0", "max_pv":"0", "pv_count":"2", "vg_missing_pv_count":"0", "lv_count":"6", "snap_count":"0", "vg_seqno":"31", "vg_tags":"", "vg_profile":"", "vg_mda_count":"2", "vg_mda_used_count":"2", "vg_mda_free":"1005", "vg_mda_size":"2040", "vg_mda_copies":"unmanaged", "vg_name":"vg_raid_1tb"},
{"vg_fmt":"lvm2", "vg_uuid":"IDvCvO-SnRm-eWIN-yhnd-Aa4P-GLsa-Due1Jy", "vg_name":"vg_raid_2tb", "vg_attr":"wz--n-", "vg_permissions":"writeable", "vg_extendable":"extendable", "vg_exported":"", "vg_autoactivation":"enabled", "vg_partial":"", "vg_allocation_policy":"normal", "vg_clustered":"", "vg_shared":"", "vg_size":"3873554432", "vg_free":"727908352","vg_sysid":"", "vg_systemid":"", "vg_lock_type":"", "vg_lock_args":"", "vg_extent_size":"8192", "vg_extent_count":"472846","vg_free_count":"88856", "max_lv":"0", "max_pv":"0", "pv_count":"1", "vg_missing_pv_count":"0", "lv_count":"4", "snap_count":"0", "vg_seqno":"12", "vg_tags":"", "vg_profile":"", "vg_mda_count":"1", "vg_mda_used_count":"1", "vg_mda_free":"1014", "vg_mda_size":"2040", "vg_mda_copies":"unmanaged", "vg_name":"vg_raid_2tb"}
]}]}
'''.strip(),
    ''
)

# > vgscan
# Found volume group "vg_raid_2tb" using metadata type lvm2
# Found volume group "vg_raid_1tb" using metadata type lvm2

# > vgs
# VG          #PV #LV #SN Attr   VSize  VFree
# vg_raid_1tb   2   6   0 wz--n- <1,82t <913,44g
# vg_raid_2tb   1   4   0 wz--n-  1,80t  347,09g

# _ = call_xvs('vg')
# pprint(_)

####################################################################################################

# > lvscan
# ACTIVE            '/dev/vg_raid_2tb/root_fc21' [33,96 GiB] inherit
# ACTIVE            '/dev/vg_raid_2tb/backup_2tb' [1,07 TiB] inherit
# ACTIVE            '/dev/vg_raid_2tb/isis_backup' [350,00 GiB] inherit
# ACTIVE            '/dev/vg_raid_2tb/ntfs_disk1' [16,00 GiB] inherit
#
# ACTIVE            '/dev/vg_raid_1tb/swap_0' [8,00 GiB] inherit
# ACTIVE            '/dev/vg_raid_1tb/tmp_0' [2,00 GiB] inherit
# ACTIVE            '/dev/vg_raid_1tb/root_debian' [<44,69 GiB] inherit
# ACTIVE            '/dev/vg_raid_1tb/backup_1tb' [350,00 GiB] inherit
# ACTIVE            '/dev/vg_raid_1tb/root_debian_12' [44,00 GiB] inherit
# ACTIVE            '/dev/vg_raid_1tb/ntfs_disk2' [60,00 GiB] inherit

# > lvdisplay
# --- Logical volume ---
# LV Path                /dev/vg_raid_2tb/root_fc21
# LV Name                root_fc21
# VG Name                vg_raid_2tb
# LV UUID                YEYY03-lAQS-YYEJ-dpT6-uyNc-4pVc-ygliM3
# LV Write Access        read/write
# LV Creation host, time localhost, 2015-05-21 17:08:46 +0200
# LV Status              available
# # open                 0
# LV Size                33,96 GiB
# Current LE             8694
# Segments               2
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:2

# --- Logical volume ---
# LV Path                /dev/vg_raid_2tb/backup_2tb
# LV Name                backup_2tb
# VG Name                vg_raid_2tb
# LV UUID                YYA8se-R2To-pStn-srDm-U6lp-eJ7v-RmQJpq
# LV Write Access        read/write
# LV Creation host, time pc9.home, 2015-05-21 17:40:41 +0200
# LV Status              available
# # open                 0
# LV Size                1,07 TiB
# Current LE             281600
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:3

# --- Logical volume ---
# LV Path                /dev/vg_raid_2tb/isis_backup
# LV Name                isis_backup
# VG Name                vg_raid_2tb
# LV UUID                eWxT9t-kXcJ-pW5q-xGAo-jJKh-xfpB-uy01bs
# LV Write Access        read/write
# LV Creation host, time osiris, 2020-06-01 02:08:08 +0200
# LV Status              available
# # open                 0
# LV Size                350,00 GiB
# Current LE             89600
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:4

# --- Logical volume ---
# LV Path                /dev/vg_raid_2tb/ntfs_disk1
# LV Name                ntfs_disk1
# VG Name                vg_raid_2tb
# LV UUID                vzyuT0-OQy2-lPLV-s5hi-JOhN-k2EO-NsbW1T
# LV Write Access        read/write
# LV Creation host, time osiris, 2020-06-11 20:06:03 +0200
# LV Status              available
# # open                 0
# LV Size                16,00 GiB
# Current LE             4096
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:5

# --- Logical volume ---
# LV Path                /dev/vg_raid_1tb/swap_0
# LV Name                swap_0
# VG Name                vg_raid_1tb
# LV UUID                4wjjHd-Nzko-aYT1-oS5l-R7mY-X0kr-PVc5E0
# LV Write Access        read/write
# LV Creation host, time bastion1.genomicvision.local, 2012-11-20 00:59:51 +0100
# LV Status              available
# # open                 2
# LV Size                8,00 GiB
# Current LE             256
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:0

# --- Logical volume ---
# LV Path                /dev/vg_raid_1tb/tmp_0
# LV Name                tmp_0
# VG Name                vg_raid_1tb
# LV UUID                8NUMaG-Qqw8-DRBd-6hHv-nzM7-Fb3O-vQ9nxV
# LV Write Access        read/write
# LV Creation host, time bastion1.genomicvision.local, 2012-11-20 00:59:51 +0100
# LV Status              available
# # open                 1
# LV Size                2,00 GiB
# Current LE             64
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:1

# --- Logical volume ---
# LV Path                /dev/vg_raid_1tb/root_debian
# LV Name                root_debian
# VG Name                vg_raid_1tb
# LV UUID                gwUUik-dm0e-UeW3-lZbL-A0t5-WQqM-zEVkls
# LV Write Access        read/write
# LV Creation host, time osiris, 2020-03-13 23:29:39 +0100
# LV Status              available
# # open                 0
# LV Size                <44,69 GiB
# Current LE             1430
# Mirrored volumes       2
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:10

# --- Logical volume ---
# LV Path                /dev/vg_raid_1tb/backup_1tb
# LV Name                backup_1tb
# VG Name                vg_raid_1tb
# LV UUID                LfY9d7-e9h2-cHvB-Gi5L-4YhX-nOYw-r0IYrv
# LV Write Access        read/write
# LV Creation host, time osiris, 2020-04-01 00:00:49 +0200
# LV Status              available
# # open                 0
# LV Size                350,00 GiB
# Current LE             11200
# Mirrored volumes       2
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:15

# --- Logical volume ---
# LV Path                /dev/vg_raid_1tb/root_debian_12
# LV Name                root_debian_12
# VG Name                vg_raid_1tb
# LV UUID                kk4ELG-SWWr-DrEN-jpbp-mSjm-Tj3r-Q8GcCs
# LV Write Access        read/write
# LV Creation host, time osiris, 2024-11-18 23:48:39 +0100
# LV Status              available
# # open                 1
# LV Size                44,00 GiB
# Current LE             1408
# Mirrored volumes       2
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:20

# --- Logical volume ---
# LV Path                /dev/vg_raid_1tb/ntfs_disk2
# LV Name                ntfs_disk2
# VG Name                vg_raid_1tb
# LV UUID                TFAfNe-MXBY-iWaT-kTTt-DcAO-1Zh7-v3K1l0
# LV Write Access        read/write
# LV Creation host, time osiris, 2024-11-19 19:16:08 +0100
# LV Status              available
# # open                 0
# LV Size                60,00 GiB
# Current LE             1920
# Segments               1
# Allocation             inherit
# Read ahead sectors     auto
# - currently set to     256
# Block device           253:21

MOCKUP_CACHE.add_cmd_mockup(
    ('/usr/bin/lvs', '--units=b', '--nosuffix', '--options=lv_all,vg_name', '--reportformat=json_std'),
    '''
{
"report": [
{
"lv": [
{"lv_uuid":"LfY9d7-e9h2-cHvB-Gi5L-4YhX-nOYw-r0IYrv", "lv_name":"backup_1tb", "lv_full_name":"vg_raid_1tb/backup_1tb", "lv_path":"/dev/vg_raid_1tb/backup_1tb", "lv_dm_path":"/dev/mapper/vg_raid_1tb-backup_1tb", "lv_parent":"", "lv_layout":"raid,raid1", "lv_role":"public", "lv_initial_image_sync":"initial image sync", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"734003200", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"0", "raid_sync_action":"idle", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2020-04-01 00:00:49 +0200", "lv_time_removed":"", "lv_host":"osiris", "lv_modules":"raid", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"15", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"100,00", "sync_percent":"100,00", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"rwi-a-r---", "vg_name":"vg_raid_1tb"},
{"lv_uuid":"TFAfNe-MXBY-iWaT-kTTt-DcAO-1Zh7-v3K1l0", "lv_name":"ntfs_disk2", "lv_full_name":"vg_raid_1tb/ntfs_disk2", "lv_path":"/dev/vg_raid_1tb/ntfs_disk2", "lv_dm_path":"/dev/mapper/vg_raid_1tb-ntfs_disk2", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"125829120", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2024-11-19 19:16:08 +0100", "lv_time_removed":"", "lv_host":"osiris", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"21", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-a-----", "vg_name":"vg_raid_1tb"},
{"lv_uuid":"gwUUik-dm0e-UeW3-lZbL-A0t5-WQqM-zEVkls", "lv_name":"root_debian", "lv_full_name":"vg_raid_1tb/root_debian", "lv_path":"/dev/vg_raid_1tb/root_debian", "lv_dm_path":"/dev/mapper/vg_raid_1tb-root_debian", "lv_parent":"", "lv_layout":"raid,raid1", "lv_role":"public", "lv_initial_image_sync":"initial image sync", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"93716480", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"","lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"0", "raid_sync_action":"idle","raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2020-03-13 23:29:39 +0100", "lv_time_removed":"", "lv_host":"osiris", "lv_modules":"raid", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"10", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"100,00", "sync_percent":"100,00", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"rwi-a-r---", "vg_name":"vg_raid_1tb"},
{"lv_uuid":"kk4ELG-SWWr-DrEN-jpbp-mSjm-Tj3r-Q8GcCs", "lv_name":"root_debian_12", "lv_full_name":"vg_raid_1tb/root_debian_12", "lv_path":"/dev/vg_raid_1tb/root_debian_12", "lv_dm_path":"/dev/mapper/vg_raid_1tb-root_debian_12", "lv_parent":"", "lv_layout":"raid,raid1", "lv_role":"public", "lv_initial_image_sync":"initial image sync", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"92274688", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"0", "raid_sync_action":"idle", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2024-11-18 23:48:39 +0100", "lv_time_removed":"", "lv_host":"osiris", "lv_modules":"raid", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"20", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"open", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"100,00", "sync_percent":"100,00", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"rwi-aor---", "vg_name":"vg_raid_1tb"},
{"lv_uuid":"4wjjHd-Nzko-aYT1-oS5l-R7mY-X0kr-PVc5E0", "lv_name":"swap_0", "lv_full_name":"vg_raid_1tb/swap_0", "lv_path":"/dev/vg_raid_1tb/swap_0", "lv_dm_path":"/dev/mapper/vg_raid_1tb-swap_0", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"16777216", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2012-11-20 00:59:51 +0100", "lv_time_removed":"", "lv_host":"bastion1.genomicvision.local", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"0", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"open", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-ao----", "vg_name":"vg_raid_1tb"},
{"lv_uuid":"8NUMaG-Qqw8-DRBd-6hHv-nzM7-Fb3O-vQ9nxV", "lv_name":"tmp_0", "lv_full_name":"vg_raid_1tb/tmp_0","lv_path":"/dev/vg_raid_1tb/tmp_0", "lv_dm_path":"/dev/mapper/vg_raid_1tb-tmp_0", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"4194304", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"","move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2012-11-20 00:59:51 +0100", "lv_time_removed":"", "lv_host":"bastion1.genomicvision.local", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"1", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"open", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-ao----", "vg_name":"vg_raid_1tb"},
{"lv_uuid":"YYA8se-R2To-pStn-srDm-U6lp-eJ7v-RmQJpq", "lv_name":"backup_2tb", "lv_full_name":"vg_raid_2tb/backup_2tb", "lv_path":"/dev/vg_raid_2tb/backup_2tb", "lv_dm_path":"/dev/mapper/vg_raid_2tb-backup_2tb", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"2306867200", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"","lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2015-05-21 17:40:41 +0200", "lv_time_removed":"", "lv_host":"pc9.home", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"3", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-a-----", "vg_name":"vg_raid_2tb"},
{"lv_uuid":"eWxT9t-kXcJ-pW5q-xGAo-jJKh-xfpB-uy01bs", "lv_name":"isis_backup", "lv_full_name":"vg_raid_2tb/isis_backup", "lv_path":"/dev/vg_raid_2tb/isis_backup", "lv_dm_path":"/dev/mapper/vg_raid_2tb-isis_backup", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"734003200", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2020-06-01 02:08:08 +0200", "lv_time_removed":"", "lv_host":"osiris", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"4", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-a-----", "vg_name":"vg_raid_2tb"},
{"lv_uuid":"vzyuT0-OQy2-lPLV-s5hi-JOhN-k2EO-NsbW1T", "lv_name":"ntfs_disk1", "lv_full_name":"vg_raid_2tb/ntfs_disk1", "lv_path":"/dev/vg_raid_2tb/ntfs_disk1", "lv_dm_path":"/dev/mapper/vg_raid_2tb-ntfs_disk1", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"33554432", "lv_metadata_size":"", "seg_count":"1", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2020-06-11 20:06:03 +0200", "lv_time_removed":"", "lv_host":"osiris", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"5", "lv_kernel_read_ahead":"256", "lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"","cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-a-----", "vg_name":"vg_raid_2tb"},
{"lv_uuid":"YEYY03-lAQS-YYEJ-dpT6-uyNc-4pVc-ygliM3", "lv_name":"root_fc21", "lv_full_name":"vg_raid_2tb/root_fc21", "lv_path":"/dev/vg_raid_2tb/root_fc21", "lv_dm_path":"/dev/mapper/vg_raid_2tb-root_fc21", "lv_parent":"", "lv_layout":"linear", "lv_role":"public", "lv_initial_image_sync":"", "lv_image_synced":"", "lv_merging":"", "lv_converting":"", "lv_allocation_policy":"inherit", "lv_allocation_locked":"", "lv_fixed_minor":"", "lv_skip_activation":"", "lv_autoactivation":"enabled", "lv_when_full":"", "lv_active":"active", "lv_active_locally":"active locally", "lv_active_remotely":"", "lv_active_exclusively":"active exclusively", "lv_major":"-1", "lv_minor":"-1", "lv_read_ahead":"auto", "lv_size":"71221248", "lv_metadata_size":"", "seg_count":"2", "origin":"", "origin_uuid":"", "origin_size":"", "lv_ancestors":"", "lv_full_ancestors":"", "lv_descendants":"", "lv_full_descendants":"", "raid_mismatch_count":"", "raid_sync_action":"", "raid_write_behind":"", "raid_min_recovery_rate":"", "raid_max_recovery_rate":"", "raidintegritymode":"", "raidintegrityblocksize":"-1", "integritymismatches":"", "move_pv":"", "move_pv_uuid":"", "convert_lv":"", "convert_lv_uuid":"", "mirror_log":"", "mirror_log_uuid":"", "data_lv":"", "data_lv_uuid":"", "metadata_lv":"", "metadata_lv_uuid":"", "pool_lv":"", "pool_lv_uuid":"", "lv_tags":"", "lv_profile":"", "lv_lockargs":"", "lv_time":"2015-05-21 17:08:46 +0200", "lv_time_removed":"", "lv_host":"localhost", "lv_modules":"", "lv_historical":"", "writecache_block_size":"-1", "lv_kernel_major":"253", "lv_kernel_minor":"2", "lv_kernel_read_ahead":"256","lv_permissions":"writeable", "lv_suspended":"", "lv_live_table":"live table present", "lv_inactive_table":"", "lv_device_open":"", "data_percent":"", "snap_percent":"", "metadata_percent":"", "copy_percent":"", "sync_percent":"", "cache_total_blocks":"", "cache_used_blocks":"", "cache_dirty_blocks":"", "cache_read_hits":"", "cache_read_misses":"", "cache_write_hits":"", "cache_write_misses":"", "kernel_cache_settings":"", "kernel_cache_policy":"", "kernel_metadata_format":"", "lv_health_status":"", "kernel_discards":"", "lv_check_needed":"unknown", "lv_merge_failed":"unknown", "lv_snapshot_invalid":"unknown", "vdo_operating_mode":"", "vdo_compression_state":"", "vdo_index_state":"", "vdo_used_size":"", "vdo_saving_percent":"", "writecache_total_blocks":"", "writecache_free_blocks":"", "writecache_writeback_blocks":"", "writecache_error":"", "lv_attr":"-wi-a-----", "vg_name":"vg_raid_2tb"}
]}]}
'''.strip(),
    ''
)

# _ = call_xvs('lv')
# pprint(_)

####################################################################################################

lvm = LVM()
for vg in lvm.vgs:
    print()
    print('-'*50)
    print(f"VG {vg.name}")
    print(f"{vg.number_of_extents:_} / {vg.number_of_free_extents:_} extents of {vg.extent_hsize}")
    print(f"{vg.hsize} / {vg.hfree}")
    _ = ' '.join([pv.name for pv in vg.pvs])
    print(f"PV: {_}")

    for lv in vg.lvs:
        print('-'*10)
        print(f"LV {lv.name}")
        print(f"layout: {lv.layout}")
        print(f"{lv.hsize}   on {lv.number_of_segments} segments")

for pv in lvm.pvs:
    print()
    print('-'*50)
    print(f"PV {pv.name} / {pv.vg_name}")
    print(f"{pv.number_of_extents:_} / {pv.number_of_free_extents:_} extents")
    print(f"{pv.hsize} / {pv.hfree}")
    start = 0

    def print_segment(start: int, end: int, name: str = None) -> None:
        size = end - start + 1
        if name is None:
            name = "free segments"
        print(f"{start:9_} — {end:9_} / {size:9_} : {name}")

    for sg in pv.segments:
        if sg.start != start:
            end = sg.start - 1
            print_segment(start, end)
        print_segment(sg.start, sg.end, sg.name)
        start = sg.end + 1
    if start != pv.number_of_extents:
        end = pv.number_of_extents - 1
        print_segment(start, end)
