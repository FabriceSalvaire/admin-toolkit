####################################################################################################

__all__ = ['is_root', 'raise_if_not_root', 'RootPermissionRequired']

####################################################################################################

import getpass

####################################################################################################

def is_root() -> bool:
    user = getpass.getuser()
    # print(user)
    return user == 'root'

####################################################################################################

class RootPermissionRequired(NameError):
    pass

def raise_if_not_root(message: str) -> None:
    if not is_root():
        raise RootPermissionRequired(f'Root privileges are required for: {message}')
