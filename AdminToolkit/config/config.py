####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from pathlib import Path

####################################################################################################

DEBUG = False
MOCKUP = False
# MOCKUP = True

####################################################################################################

SOURCE = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path('~/.config/admin-toolkit').expanduser()

CLI_COMMANDS_PATH = SOURCE.parent.joinpath('CliCommands')
if not CLI_COMMANDS_PATH.exists():
    CLI_COMMANDS_PATH = CONFIG_PATH.joinpath('CliCommands')
CLI_COMMANDS_PATH = CLI_COMMANDS_PATH.resolve()
if not CLI_COMMANDS_PATH.exists():
    print(f"source: {SOURCE}")
    print(f"config: {CONFIG_PATH}")
    raise NameError(f"CliCommands not found {CLI_COMMANDS_PATH}")
