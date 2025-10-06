####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['main']

####################################################################################################

import sys

####################################################################################################

def main() -> None:
    query = ' '.join(sys.argv[1:])
    if query:
        from AdminToolkit.cli import Cli
        from AdminToolkit.config import config

        cli = Cli(config.CLI_COMMANDS_PATH)
        cli.start(query)
