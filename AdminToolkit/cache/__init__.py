####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""
This module provides the CliCache class for in-memory and persistent caching of objects
used by the AdminToolkit CLI. It supports storing, retrieving, deleting, saving, and loading
cached data using pickle serialization.
"""

__all__ = ['CliCache']

####################################################################################################

from pathlib import Path
from typing import Any, Iterator

import pickle

####################################################################################################

class CliCache:

    ##############################################

    def __init__(self) -> None:
        """
        Initialize an empty cache dictionary.
        """
        self._cache = {}

    ##############################################

    def __iter__(self) -> Iterator[[str, Any]]:
        return iter(self._cache.items())

    @property
    def names(self) -> Iterator[str]:
        """
        Return an iterator over the names of cached items.
        """
        return self._cache.keys()

    ##############################################

    def store(self, name: str, value: Any = None) -> None:
        """
        Store a value in the cache under the given name.
        """
        self._cache[name] = value

    def get(self, name: str) -> Any:
        """
        Retrieve a value from the cache by name. Returns None if not found.
        """
        # return self._cache[name]
        return self._cache.get(name, None)

    def delete(self, name: str) -> None:
        """
        Delete a cached item by name.
        """
        try:
            del self._cache[name]
        except KeyError:
            pass

    ##############################################

    def save(self, name: str, path: Path | str) -> None:
        """
        Serialize and save a cached item to disk using pickle.
        """
        path = Path(path)
        data = self.get(name)
        if data:
            _ = pickle.dumps(data)
            path.write_bytes(_)

    def load(self, name: str, path: Path | str) -> Any:
        """
        Load a cached item from disk, deserialize it, and store it in the cache.
        Returns the loaded data.
        """
        path = Path(path)
        # if path.exists():
        _ = path.read_bytes()
        data = pickle.loads(_)
        self.store(name, data)
        return data
