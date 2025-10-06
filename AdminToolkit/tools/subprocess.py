####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['RUN_DANGEROUS', 'run_command', 'iter_on_command_output']

####################################################################################################

import json
import subprocess
import sys

from AdminToolkit.config.config import DEBUG
from AdminToolkit.printer import atprint
from AdminToolkit.tools.mockup import MOCKUP_CACHE
from AdminToolkit.tools.object import load_json

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
    except Exception as e:
         raise e

####################################################################################################

def run_command(
    cmd: list[str],
    to_json: bool = False,
    cls_map: dict = None,
    to_bytes: bool = False,
    print_output: bool = False,
    check: bool = True,
    rc: bool = False,
) -> str:
    if DEBUG:
        atprint(f'<red>run_command:</red> {cmd}')
    _ = MOCKUP_CACHE.get(cmd)
    if _ is not None:
        stdout = _.stdout
        stderr = _.stderr
    else:
        process = subprocess.run(cmd, capture_output=True, check=check)
        stdout = process.stdout
        stderr = process.stderr
    if print_output or DEBUG:
        def _print(_):
            if isinstance(_, bytes):
                try:
                    _ = _.decode('utf8')
                    atprint(_)
                except UnicodeDecodeError:
                    pass
        LRULE = '<blue>-- '
        RRULE = '-'*30 + '</blue>'
        atprint(f'{LRULE} stderr {RRULE}')
        _print(stderr)
        atprint(f'{LRULE} stdout {RRULE}')
        _print(stdout)
        atprint('<blue>' + '-'*50 + '</blue>')
    if rc:
        return process.returncode
    if to_bytes:
        return stdout
    if isinstance(stdout, bytes):
        stdout = stdout.decode('utf8')
    if to_json:
        try:
            # return json.loads(stdout)
            return load_json(stdout, cls_map)
        except json.decoder.JSONDecodeError:
            raise NameError(f'{cmd} -> {stdout}')
    return stdout

####################################################################################################

def iter_on_command_output(cmd: list[str], skip_first_lines: int = 0) -> str:
    output = run_command(cmd)
    for i, line in enumerate(output.splitlines()):
        if i >= skip_first_lines:
            yield line
