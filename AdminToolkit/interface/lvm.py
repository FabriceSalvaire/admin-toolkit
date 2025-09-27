####################################################################################################

from collections import namedtuple
from pathlib import Path
from pprint import pprint
import subprocess
import json

from AdminToolkit.tools.object import to_namedtuple

####################################################################################################

PVDISPLAY = '/usr/bin/pvdisplay'
XVS = '/usr/bin/{}s'

####################################################################################################

def call_xvs(name: str) -> list:
    cmd = (
        XVS.format(name),
        '--units=s',
        '--nosuffix',
        f'--options={name}_all,vg_name',
        '--reportformat=json_std',
    )
    process = subprocess.run(cmd, capture_output=True)
    _ = process.stdout.decode('utf8')
    _ = json.loads(_)
    data = _['report'][0][name]
    cls_name = f'{name.capitalize()}Info'
    return [to_namedtuple(cls_name, _) for _ in data]

####################################################################################################


if __name__ == '__main__':
    for type_ in ('pv', 'vg', 'lv'):
        print('-'*10)
        _ = call_xvs(type_)
        pprint(_)
