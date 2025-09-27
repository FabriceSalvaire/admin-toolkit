####################################################################################################

__all__ = ['RUN_DANGEROUS', 'run_command', 'iter_on_command_output']

####################################################################################################

import json
import subprocess

from AdminToolkit.printer import atprint

####################################################################################################

def RUN_DANGEROUS(message: str, cmd: list[str], **kwargs) -> str:
    from AdminToolkit.danger import CONFIRM_DANGER, AbortAction
    try:
        warning = '/!\\ You will run this dangerous command: /!\\'
        atprint('<red>' + '='*len(warning) + '</red>')
        atprint('<red>' + warning + '</red>')
        atprint('<blue>' + ' '.join(cmd) + '</blue>')
        # This will abort by raising AbortAction
        CONFIRM_DANGER(message)
        # else we go !!!
        return run_command(cmd, **kwargs)
    except AbortAction:
        raise
    except Exception:
        raise

####################################################################################################

def run_command(cmd: list[str], to_json: bool = False, to_bytes: bool = False) -> str:
    process = subprocess.run(cmd, capture_output=True)
    _ = process.stdout
    if to_bytes:
        return _
    _ = _.decode('utf8')
    if to_json:
        try:
            return json.loads(_)
        except json.decoder.JSONDecodeError:
            raise NameError(f'{cmd} -> {_}')
    return _

####################################################################################################

def iter_on_command_output(cmd: list[str], skip_first_lines: int = 0) -> str:
    output = run_command(cmd)
    for i, line in enumerate(output.splitlines()):
        if i >= skip_first_lines:
            yield line
