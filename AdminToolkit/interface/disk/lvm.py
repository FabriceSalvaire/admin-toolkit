####################################################################################################

# from collections import namedtuple
# from pathlib import Path
from pprint import pprint

from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.tools.object import to_namedtuple
from AdminToolkit.tools.subprocess import run_command

####################################################################################################

PVDISPLAY = '/usr/bin/pvdisplay'
XVS = '/usr/bin/{}s'

####################################################################################################

def call_xvs(name: str) -> list:
    raise_if_not_root()
    cmd = (
        XVS.format(name),
        '--units=s',
        '--nosuffix',
        f'--options={name}_all,vg_name',
        '--reportformat=json_std',
    )
    _ = run_command(cmd, to_json=True)
    data = _['report'][0][name]
    cls_name = f'{name.capitalize()}Info'
    return [to_namedtuple(cls_name, _) for _ in data]

####################################################################################################


if __name__ == '__main__':
    for type_ in ('pv', 'vg', 'lv'):
        print('-'*10)
        _ = call_xvs(type_)
        pprint(_)
