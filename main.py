####################################################################################################

from pathlib import Path

from AdminToolkit.cli import Cli

####################################################################################################

SOURCE = Path(__file__).parent
COMMANDS_PATH = SOURCE.joinpath('CliCommands')
print(f'commands: {COMMANDS_PATH}')

####################################################################################################

cli = Cli(COMMANDS_PATH)
cli.start()
