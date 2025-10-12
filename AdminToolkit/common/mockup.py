####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = [
    'CmdMockupCacheEntry',
    'FileMockupCacheEntry',
    'MOCKUP_CACHE',
    'MockupCacheEntry',
    'MockupPath',
]

####################################################################################################

from dataclasses import dataclass
from pathlib import Path

from AdminToolkit.config import config
from AdminToolkit.common.printer import atprint

####################################################################################################

class MockupCacheEntry:
    pass

####################################################################################################

@dataclass
class CmdMockupCacheEntry:
    cmd: list
    stdout: str
    stderr: str = ''

    ##############################################

    @property
    def str(self) -> str:
        return str(self.cmd)

    @property
    def uuid(self) -> int:
        return MockupCache.to_uuid(self.cmd)

####################################################################################################

@dataclass
class FileMockupCacheEntry:
    path: str
    content: str

    ##############################################

    @property
    def str(self) -> str:
        return str(self.path)

    @property
    def uuid(self) -> int:
        return MockupCache.to_uuid(self.path)

####################################################################################################

class MockupCache:

    ##############################################

    def __init__(self) -> None:
        self._cache = {}

    ##############################################

    @classmethod
    def to_uuid(cls, key) -> int:
        return hash(key)

    ##############################################

    def _add_entry(self, entry: MockupCacheEntry) -> None:
        uuid = entry.uuid
        if uuid not in self._cache:
            self._cache[uuid] = entry
        else:
            raise ValueError(f"Entry is already in mockup cache {entry}")

    ##############################################

    def add_cmd_mockup(self, *args, **kwargs) -> None:
        entry = CmdMockupCacheEntry(*args, **kwargs)
        self._add_entry(entry)

    def add_file_mockup(self, *args, **kwargs) -> None:
        entry = FileMockupCacheEntry(*args, **kwargs)
        self._add_entry(entry)

    ##############################################

    def get(self, key) -> MockupCacheEntry:
        if config.MOCKUP:
            import AdminToolkit.config.mockup_config
            atprint(f"<blue>Lookup mockup for</blue> {key}")
            uuid = self.to_uuid(key)
            _ = self._cache.get(uuid, None)
            if _ is not None:
                atprint(f"<red>Found mockup for</red> {key}")
            return _
        return None

    ##############################################

    def read_text(self, path: Path) -> str:
        path = Path(path)
        entry = self.get(path)
        if entry is not None:
            return entry.content
        return path.read_text()

    ##############################################

    # for run_command see subprocess.py

####################################################################################################

class MockupPath(Path):

    ##############################################

    def read_text(self) -> str:
        content = MOCKUP_CACHE.read_text(self)
        if config.DEBUG:
            RULE = '<blue>' + '-'*50 + '</blue>'
            atprint(RULE)
            print(content)
            atprint(RULE)
        return content

####################################################################################################


MOCKUP_CACHE = MockupCache()
