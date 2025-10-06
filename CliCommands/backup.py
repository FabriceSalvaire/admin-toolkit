####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

# Fixme: raise aborterror

__all__ = ['Backup']

####################################################################################################

from pprint import pprint

from pathlib import Path

from AdminToolkit.config import config
from AdminToolkit.cli import CommandGroup
from AdminToolkit.interface.disk.mount import mount, is_mounted, umount
from AdminToolkit.tools.object import objectify

####################################################################################################

class Backup(CommandGroup):

    CONFIG_PATH = config.CONFIG_PATH.joinpath('backup')

    ##############################################

    @classmethod
    def _load_backup_config(cls) -> dict:
        import yaml
        config_path = Backup.CONFIG_PATH.joinpath('config.yaml')
        conf = yaml.load(config_path.read_text(), Loader=yaml.SafeLoader)
        # pprint(conf)
        for name, data in conf.items():
            obj = objectify('BackupConfig', data)
            conf[name] = obj
            if hasattr(obj, 'tasks'):
                for name, data in obj.tasks.items():
                    _ = objectify('BackupTask', data)
                    obj.tasks[name] = _
        # pprint(conf)
        return conf

    ##############################################

    @classmethod
    def _backup_config(cls, name: str) -> dict:
        backup_config = Backup._load_backup_config()
        try:
            return backup_config[name]
        except KeyError:
            raise NameError(f"Unknown backup {name}")

    ##############################################

    def check_rsync_filter(self, name: str) -> None:
        from AdminToolkit.backup.rsync import RsyncBackup
        # _, filter_path = Backup._backup_config(name)
        # self.print(f"Filter is <green>{filter_path}</green>")
        # RsyncBackup.check_filter(filter_path)

    ##############################################

    def backup(self, name: str = None) -> None:
        if name is None:
            conf = Backup._load_backup_config()
            for name in sorted(conf.keys()):
                self.print(f"  {name}")
            return

        from AdminToolkit.backup.rsync import RsyncBackup

        conf = Backup._backup_config(name)
        # pprint(conf)

        device = Path(conf.device)
        # Check device is online
        if not device.exists():
            self.print(f"device <blue>{conf.device}</blue> is <red>unplugged</red>")
            return
        sd_device = Path(conf.device).resolve()
        self.print(f"device: <blue>{conf.device}</blue> -> <green>{sd_device}</green>")

        mount_point = Path(conf.mount_point)
        # Check mount point exists and is not invalid
        if not mount_point.exists():
            self.print(f"mount point <blue>{mount_point}</blue> <red>doesn't exists</red>")
            return
        self.print(f"mount point: <blue>{mount_point}</blue>")
        if str(mount_point) == '/':
            self.print(f"Invalid mount point <red>{mount_point}</red>")
            return
        if is_mounted(device, mount_point):
            self.print(f"  is already mounted")
        else:
            mount(device, mount_point)
            if not is_mounted(device, mount_point):
                raise NameError("mount error...")
            self.print(f"  mounted")

        for name, task in conf.tasks.items():
            self.print(f"Task <red>{name:15}</red>")
            source = Path(task.source)
            if not source.exists():
                self.print(f"source <red>{source}</red> doesn't exists")
                return
            str_source = str(source)
            # ensure source has a trailing /
            if not str_source.endswith('/'):
                str_source += '/'
            target = mount_point.joinpath(task.target)
            # we don't check target exists
            if str(target) == '/':
                self.print(f"Invalid target <red>{target}</red>")
                return
            self.print(f"  <blue>{str_source:30}</blue> -> <green>{target}</green>")
            self.print()
            filter_path = Backup.CONFIG_PATH.joinpath('filters', task.filter)
            if not filter_path.exists():
                self.print(f"filter <red>{filter_path}</red> doesn't exists")
                return
            self.print(f"  filter: <green>{filter_path}</green>")
            options = task.options.split() if hasattr(task, 'options') else ()
            self.print(f"  options: <green>{options}</green>")
        # _ = RsyncBackup(backup_path, filter_path)
        # _.run()

        umount(device, mount_point)
        self.print(f"Unmounted <blue>{mount_point}</blue>")
