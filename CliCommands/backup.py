####################################################################################################

__all__ = ['Backup']

####################################################################################################

# from pprint import pprint

from pathlib import Path

from AdminToolkit.cli import CommandGroup

####################################################################################################

SOURCE_PATH = Path(__file__).resolve().parents[1]

####################################################################################################

class Backup(CommandGroup):

    ##############################################

    def _load_backup_config(self) -> dict:
        import yaml
        config_path = SOURCE_PATH.joinpath('backup', 'config.yaml')
        backup_config = yaml.load(config_path.read_text(), Loader=yaml.SafeLoader)
        return backup_config

    ##############################################

    def _backup_config(self, name: str) -> list[Path]:
        backup_config = self._load_backup_config()
        config = backup_config[name]
        backup_path = config['backup_path']
        filter_path = SOURCE_PATH.joinpath('backup', 'filters', config['filter'])
        return backup_path, filter_path

    ##############################################

    def check_rsync_filter(self, name: str) -> None:
        from AdminToolkit.backup.rsync import RsyncBackup
        _, filter_path = self._backup_config(name)
        self.print(f"Filter is <green>{filter_path}</green>")
        RsyncBackup.check_filter(filter_path)

    ##############################################

    def backup(self, name: str) -> None:
        from AdminToolkit.backup.rsync import RsyncBackup
        backup_path, filter_path = self._backup_config(name)
        self.print(f"Backup target is <green>{backup_path}</green>")
        self.print(f"Filter is <green>{filter_path}</green>")
        _ = RsyncBackup(backup_path, filter_path)
        _.run()
