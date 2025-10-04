####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

"""du interface

"""

####################################################################################################

from pathlib import Path

from AdminToolkit.tools.subprocess import iter_on_command_output

####################################################################################################

DU = '/usr/bin/du'

####################################################################################################

def du(path: Path | str) -> int:
    # -0, --null
    # end each output line with NUL, not newline
    #
    # -a, --all
    # write counts for all files, not just directories
    #
    # --apparent-size
    # print apparent sizes rather than device usage; although the apparent size is usually smaller,
    # it may be larger due to holes in ('sparse') files, internal fragmentation, indirect blocks, and the like
    #
    # -B, --block-size=SIZE
    # scale sizes by SIZE before printing them; e.g., '-BM' prints sizes in units of 1,048,576 bytes;
    # see SIZE forat below
    #
    # -b, --bytes
    # equivalent to '--apparent-size --block-size=1'
    #
    # -c, --total
    # produce a grand total
    #
    # -D, --dereference-args
    # dereference only symlinks that are listed on the command line
    #
    # -d, --max-depth=N
    # print the total for a directory (or file, with --all) only if it is N or fewer levels below the command line
    # argument; --max-depth=0 is the same as --summarize
    #
    # --files0-from=F
    # summarize device usage of the NUL-terminated file names specified in file F; if F is -, then read names from
    # standard input
    #
    # -H
    # equivalent to --dereference-args (-D)
    #
    # -h, --human-readable
    # print sizes in human readable format (e.g., 1K 234M 2G)
    #
    # --inodes
    # list inode usage information instead of block usage
    #
    # -k
    # like --block-size=1K
    #
    # -L, --dereference
    # dereference all symbolic links
    #
    # -l, --count-links
    # count sizes many times if hard linked
    #
    # -m
    # like --block-size=1M
    #
    # -P, --no-dereference
    # don't follow any symbolic links (this is the default)
    #
    # -S, --separate-dirs
    # for directories do not include size of subdirectories
    #
    # --si
    # like -h, but use powers of 1000 not 1024
    #
    # -s, --summarize
    # display only a total for each argument
    #
    # -t, --threshold=SIZE
    # exclude entries smaller than SIZE if positive, or entries greater than SIZE if negative
    #
    # --time
    # show time of the last modification of any file in the directory, or any of its subdirectories
    #
    # --time=WORD
    # show time as WORD instead of modification time: atime, access, use, ctime or status
    #
    # --time-style=STYLE
    # show times using STYLE, which can be: full-iso, long-iso, iso, or +FORMAT;
    # FORMAT is interpreted like in'date'
    #
    # -X, --exclude-from=FILE
    # exclude files that match any pattern in FILE
    #
    # --exclude=PATTERN
    # exclude files that match PATTERN
    #
    # -x, --one-file-system
    # skip directories on different file systems

    cmd = (
        DU,
        '-b',   # --bytes
        '-c',   # --total
        '-x',   # --one-file-system
        # '-h',
        str(path),
    )
    # print(cmd)
    _ = list(iter_on_command_output(cmd))
    bytes_ = int(_[-1].split()[0])
    return bytes_
