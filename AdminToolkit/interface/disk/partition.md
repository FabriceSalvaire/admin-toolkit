# GUID Partition Table (GPT)

See http://en.wikipedia.org/wiki/GUID_Partition_Table

The UEFI specification stipulates that a minimum of 16,384 bytes, regardless of sector size,
are allocated for the Partition Entry Array. Thus, on a disk with 512-byte sectors,
at least 32 sectors are used for the Partition Entry Array

| LBA0   | Protective MBR for compatibility = fake single partition of type EEh
| LBA1   | Primary GPT Header
| LBA2   | Entry1 ...
| ...    | 
| LBA33  | ... Entries128
| LBA34  | Partition1
| ...    | 
| LBA-33 | Entry1 ...
| LBA-2  | ... Entries128
| LBA-1  | Secondary GPT Header

## Partition table header (LBA 1)

**GPT header format**

|  Offset   |  Length  | Contents                                                                     |
|  0 (0x00) |  8 bytes | Signature ("EFI PART", 45h 46h 49h 20h 50h 41h 52h 54h                       |
                         or 0x5452415020494645ULL on little-endian machines)                          |
|  8 (0x08) |  4 bytes | Revision number of header - 1.0 ( 00h 00h 01h 00h ) for UEFI 2.10            |
| 12 (0x0C) |  4 bytes | Header size in little endian (in bytes, usually 5Ch 00h 00h 00h or 92 bytes) |
| 16 (0x10) |  4 bytes | CRC-32 of header (offset +0 to +0x5B) in little endian,                      |
                         with this field zeroed during calculation                                    |
| 20 (0x14) |  4 bytes | Reserved; must be zero                                                       |
| 24 (0x18) |  8 bytes | Current LBA (location of this header copy)                                   |
| 32 (0x20) |  8 bytes | Backup LBA (location of the other header copy)                               |
| 40 (0x28) |  8 bytes | First usable LBA for partitions (primary partition table last LBA + 1)       |
| 48 (0x30) |  8 bytes | Last usable LBA (secondary partition table first LBA − 1)                    |
| 56 (0x38) | 16 bytes | Disk GUID in little endian                                                   |
| 72 (0x48) |  8 bytes | Starting LBA of array of partition entries (usually 2 for compatibility)     |
| 80 (0x50) |  4 bytes | Number of partition entries in array                                         |
| 84 (0x54) |  4 bytes | Size of a single partition entry (usually 80h or 128)                        |
| 88 (0x58) |  4 bytes | CRC-32 of partition entries array in little endian                           |
| 92 (0x5C) |  *       | Reserved;                                                                    |
                         must be zeroes for the rest of the block (420 bytes for a sector size of     |
                         512 bytes; but can be more with larger sector sizes)                         |

## Partition entries (LBA 2–33)

**GUID partition entry format**

|  Offset   | Length   | Contents                                        |
|  0 (0x00) | 16 bytes | Partition type GUID (little endian )            |
| 16 (0x10) | 16 bytes | Unique partition GUID (little endian )          |
| 32 (0x20) |  8 bytes | First LBA ( little endian )                     |
| 40 (0x28) |  8 bytes | Last LBA (inclusive, usually odd)               |
| 48 (0x30) |  8 bytes | Attribute flags (e.g. bit 60 denotes read-only) |
| 56 (0x38) | 72 bytes | Partition name (36 UTF-16 LE code units)        |

**Partition attributes**
|   Bit | Content                                                                                   |
|     0 | Platform required (required by the computer to function properly,                         |
          OEM partition for example, disk partitioning utilities must preserve the partition as is) |
|     1 | EFI firmware should ignore the content of the partition and not try to read from it       |
|     2 | Legacy BIOS bootable (equivalent to active flag                                           |
          (typically bit 7 set) at offset +0h in partition entries of the MBR partition table )     |
|  3–47 | Reserved for future use                                                                   |
| 48–63 | Defined and used by the individual partition type                                         |

Microsoft defines the type-specific attributes for basic data partition as:
**Basic data partition attributes**
| Bit | Content
| 60  | Read-only
| 61  | Shadow copy (of another partition)
| 62  | Hidden
| 63  | No drive letter (i.e. do not automount)

## Partition Type GUID

| 0657FD6D-A4AB-43C4-84E5-0933C84B4F4F | Linux Swap partition
| 0FC63DAF-8483-4772-8E79-3D69D8477DE4 | Linux filesystem data
| C12A7328-F81F-11D2-BA4B-00A0C93EC93B | EFI system partition
| DE94BBA4-06D1-4D40-A16A-BFD50179D6AC | Windows Recovery Environment
| E3C9E316-0B5C-4DB8-817D-F92DF00215AE | Microsoft Reserved Partition (MSR)
| E6D6D379-F507-44C2-A23C-238F2A3DF928 | LVM
| EBD0A0A2-B9E5-4433-87C0-68B6B72699C7 | Windows Basic data partition

# MBR

LBA0 512-byte
  446 Bootstrap code area
   440 code
     4 signature
     2 0x0000
   16 Partition entry 1
   16 Partition entry 2
   16 Partition entry 3
   16 Partition entry 4
    2 MBR signature / magic number 0x55AA

**For modern standard MBR, Bootstrap is**

  218 Bootstrap code area (part 1)
      Disk Timestamp
    2   0x0000
    1   Original physical drive (0x80–0xFF)
    1   Seconds (0–59)
    1   Minutes (0–59)
    1 Hours (0–23)
  216 Bootstrap code area (part 2, code entry at 0x0000)
   or 222
      Disk Signature
    4 32-bit disk signature
    2 0x0000 (0x5A5A if copy-protected)

**Layout of a 16-byte partition entry**

| 1 | Status or physical drive                                                         |
|   | (bit 7 set is for active or bootable,                                            |
|   | old MBRs only accept 0x80, 0x00 means inactive, and 0x01–0x7F stand for invalid) |
| 3 | CHS address of first absolute sector in partition                                |
| 1 | Partition type                                                                   |
| 3 | CHS address of last absolute sector in partition                                 |
| 4 | LBA of first absolute sector in the partition                                    |
| 4 | Number of sectors in partition                                                   |

**Partition Types**
- 0x05 extended partition CHS
- 0x0F extended partition LBA

**Extended Boot Records EBR**

- EBR are chained : MBR Part -> EBR1 -> EBR2 -> ...
- same as MBR
- code, partition 2 and 3 are zeroed
