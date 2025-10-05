####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['main']

####################################################################################################

from pathlib import Path

from AdminToolkit.cli import Cli

####################################################################################################

# Fixme:
SOURCE = Path(__file__).parents[2]
COMMANDS_PATH = SOURCE.joinpath('CliCommands')
# print(f'commands: {COMMANDS_PATH}')

####################################################################################################

def main() -> None:
    cli = Cli(COMMANDS_PATH)
    cli.start()
