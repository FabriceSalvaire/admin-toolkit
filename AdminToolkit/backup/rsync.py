####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from pathlib import Path
import subprocess

from AdminToolkit.printer import atprint

####################################################################################################

RSYNC = '/usr/bin/rsync'

####################################################################################################

class RsyncBackup:

    ##############################################

    def __init__(
            self,
            backup_path: str | Path,
            filter_path: str | Path,
    ) -> None:
        self._backup_path = Path(backup_path)
        self._filter_path = Path(filter_path)
        self._check_path()
        # self.check_filter()

    ##############################################

    def _check_backup_path(self) -> None:
        if not self._backup_path.exists():
            raise ValueError(f"Backup path {self._backup_path} doesn't exists")

        backup_path = str(self._backup_path)
        # backup_path == '/'
        if not backup_path.startswith('/run/media/'):
            raise ValueError(f"Invalid backup path {self._backup_path}")

    def _check_filter_path(self) -> None:
        if not self._filter_path.exists():
            raise ValueError(f"Filter path {self._filter_path} doesn't exists")

    def _check_path(self) -> None:
        self._check_backup_path()
        self._check_filter_path()

    ##############################################

    @classmethod
    def check_filter(self, filter_path: str | Path) -> None:
        filter_path = Path(filter_path)
        if not filter_path.exists():
            atprint(f"<red>Filter path {filter_path} doesn't exists</red>")

        excluded = []
        lines = filter_path.read_text()
        for line in lines.splitlines():
            if line.startswith('-/ '):
                _, path = line.split(' ')
                path = Path(path)
                if not path.exists():
                    atprint(f"<red>don't exists:</red> <blue>{path}</blue>")
                else:
                    _ = str(path)
                    if _ not in excluded:
                        excluded.append(_)

        print()
        atprint('<red>Excluded:</red>')
        excluded.sort()
        for _ in excluded:
            left = Path(_).parts[1]
            if left in ('root', 'home', 'srv'):
                atprint(f"<blue>{_}</blue>")
            elif left in ('usr', 'var'):
                atprint(f"<green>{_}</green>")
            else:
                atprint(_)

    ##############################################

    def run(self, dry_run: bool = False, checksum: bool = False):
        self._check_path()
        cmd = [
            RSYNC,
            '--archive',
            #   same as -rlptgoD (no -A,-X,-U,-N,-H)
            #   --recursive
            #   --links
            #   --perms
            #   --times
            #   --group
            #   --owner
            #   --devices
            #   --specials
            '--hard-links',
            '--xattrs',
            # --acls
            # --atimes
            # --crtimes
            '--verbose',
            '--delete',
            '--ignore-errors',
        ]
        if checksum:
            cmd.append('--checksum')
        if dry_run:
            cmd.append('--dry-run')
        # Debug
        #   '--list-only',
        cmd += [
            # for Shell "" are required
            f'--filter=merge {self._filter_path}',
            '/',
            str(self._backup_path),
        ]
        # Fixme: func
        atprint(' '.join(cmd))
        subprocess.run(cmd)
