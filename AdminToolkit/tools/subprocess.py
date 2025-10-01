####################################################################################################

__all__ = ['RUN_DANGEROUS', 'run_command', 'iter_on_command_output']

####################################################################################################

import json
import subprocess
from dataclasses import dataclass

from AdminToolkit.printer import atprint

####################################################################################################

MOCKUP = True
DEBUG = True

@dataclass
class MockupCacheEntry:
    cmd: list
    stdout: str
    stderr: str = ''

    ##############################################
    @property
    def uuid(self) -> int:
        return MockupCache.cmd_uuid(self.cmd)


class MockupCache:

    ##############################################

    def __init__(self) -> None:
        self._cache = {}

    ##############################################

    @classmethod
    def cmd_uuid(cls, cmd: list) -> int:
        return hash(cmd)

    ##############################################

    def add_mockup_cache(self, cmd: list, stdout: str, stderr: str = '') -> None:
        uuid = self.cmd_uuid(cmd)
        # uuid = entry.uuid
        if uuid not in self._cache:
            entry = MockupCacheEntry(cmd, stdout, stderr)
            self._cache[uuid] = entry
        else:
            raise ValueError(f"Entry is already in mockup cache {cmd}")

    ##############################################

    def use_mockup(self, cmd: list) -> MockupCacheEntry:
        if MOCKUP:
            uuid = self.cmd_uuid(cmd)
            return self._cache.get(uuid, None)
        return None


_mockup_cache = MockupCache()

####################################################################################################

def RUN_DANGEROUS(message: str, cmd: list[str], **kwargs) -> str:
    from AdminToolkit.danger import CONFIRM_DANGER, AbortAction
    try:
        warning = '/!\\ You will run this dangerous command: /!\\'
        atprint('<red>' + '='*len(warning) + '</red>')
        atprint('<red>' + warning + '</red>')
        print()
        atprint('<blue>' + ' '.join(cmd) + '</blue>')
        print()
        # This will abort by raising AbortAction
        CONFIRM_DANGER(message)
        # else we go !!!
        return run_command(cmd, **kwargs)
    except AbortAction:
        raise
    except Exception:
        raise

####################################################################################################

def run_command(
    cmd: list[str],
    to_json: bool = False,
    to_bytes: bool = False,
    print_output: bool = False,
) -> str:
    if DEBUG:
        atprint(f'<red>run_command:</red> {cmd}')
    _ = _mockup_cache.use_mockup(cmd)
    if _ is not None:
        stdout = _.stdout
        stderr = _.stderr
    else:
        process = subprocess.run(cmd, capture_output=True)
        stdout = process.stdout
        if print_output:
            stderr = process.stderr.decode('utf8')
            atprint('<blue>-- stderr</blue>')
            atprint(stderr)
            atprint('<blue>-- stdout</blue>')
            atprint(stdout.decode('utf8'))
    if to_bytes:
        return stdout
    stdout = stdout.decode('utf8')
    if DEBUG:
        atprint('--- STDOUT ' + '-'*30)
        atprint(stdout)
        atprint('-'*50)
    if to_json:
        try:
            return json.loads(stdout)
        except json.decoder.JSONDecodeError:
            raise NameError(f'{cmd} -> {stdout}')
    return stdout

####################################################################################################

def iter_on_command_output(cmd: list[str], skip_first_lines: int = 0) -> str:
    output = run_command(cmd)
    for i, line in enumerate(output.splitlines()):
        if i >= skip_first_lines:
            yield line
