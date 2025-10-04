####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['atprint', 'default_print']

####################################################################################################

from enum import Enum

####################################################################################################

# \033[   [<PREFIX>];[<COLOR>];[<TEXT DECORATION>]   m

# Foreground : 0
# Bold : 1
# Background : 3
# Underscore : 4

# Basic 8 colors : 30..37
# Basic high contrast colors : 90..97
# xterm-256 colors : 0..255

# bold \e[1;30m
# underline \e[4;30m
# bg \e[40m
# high intensity \e[0;90m
# bold hi \e[1;90m
# bh hi \e[0;100m
# xterm-256 colors \033[38;5;${code}m

####################################################################################################

class Palette(Enum):
    # RESET = '\033[0m'
    RESET = '\033[39m'

    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'

####################################################################################################

# def default_print(*args, **kwargs):
def default_print(message: str) -> None:
    patterns = [
        (f'<{_.lower()}>', Palette._member_map_[_].value)
        for _ in Palette._member_names_
        if _ not in ('RESET')
    ]
    close_patterns = []
    for i, o in patterns:
        close_patterns.append((i.replace('<', '</'), Palette.RESET.value))
    patterns += close_patterns
    # print(patterns)
    for i, o in patterns:
        message = message.replace(i, o)
    print(message)

####################################################################################################

atprint = default_print
