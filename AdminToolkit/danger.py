####################################################################################################

__all__ = ['AbortAction', 'raise_if_root_device', 'CONFIRM_DANGER']

####################################################################################################

import random

from AdminToolkit.interface.disk.mount import get_root_device
from AdminToolkit.interface.user import raise_if_not_root
from AdminToolkit.printer import atprint

####################################################################################################

class AbortAction(NameError):
    pass

####################################################################################################

def raise_if_root_device(name: str):
    from AdminToolkit.interface.disk.partition import partion_to_device
    if str(get_root_device()) == str(partion_to_device(name)):
        raise AbortAction(f'Device {name} is root device')

####################################################################################################

def CONFIRM_DANGER(message: str):
    # , printer=None
    _ = str(random.random()*1000_000)
    _ = _[1] + _[3] + _[5]
    CONFIRMATION = f'YES{_}!'
    # if printer is not None:
    #     printer(CONFIRMATION)
    #     prompt = ''
    # else:
    #     prompt = message + f' (confirm with: "{CONFIRMATION}"): '
    # rc = input(prompt)
    prompt = '<red>' + message + '</red>' + f' (confirm with: "<green>{CONFIRMATION}</green>"): '
    atprint(prompt)
    rc = input()
    if rc != CONFIRMATION:
        raise AbortAction

####################################################################################################


if __name__ == '__main__':
    CONFIRM_DANGER('Test...')
