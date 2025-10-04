####################################################################################################
#
# AdminToolkit — ...
# Copyright (C) 2025 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['Cli', 'CommandGroup']

####################################################################################################

import getpass
import importlib.util
import inspect
import os
import traceback

from pathlib import Path
from pprint import pprint

# See also [cmd — Support for line-oriented command interpreters — Python documentation](https://docs.python.org/3/library/cmd.html)
# Python Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/)
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit import print_formatted_text, shortcuts
from prompt_toolkit.completion import WordCompleter, Completer, Completion, CompleteEvent
# from prompt_toolkit.document import Document
# from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
# from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.styles import Style

from AdminToolkit.danger import AbortAction
from AdminToolkit.interface.user import RootPermissionRequired

####################################################################################################

# _module_logger = logging.getLogger('')

LINESEP = os.linesep

SOURCE_PATH = Path(__file__).resolve().parents[1]

type CommandName = str

####################################################################################################

class CustomCompleter(Completer):

    """
    Simple autocompletion on a list of words.

    :param words: List of words or callable that returns a list of words.
    :param ignore_case: If True, case-insensitive completion.
    :param meta_dict: Optional dict mapping words to their meta-text. (This
        should map strings to strings or formatted text.)
    :param WORD: When True, use WORD characters.
    :param sentence: When True, don't complete by comparing the word before the
        cursor, but by comparing all the text before the cursor. In this case,
        the list of words is just a list of strings, where each string can
        contain spaces. (Can not be used together with the WORD option.)
    :param match_middle: When True, match not only the start, but also in the
                         middle of the word.
    :param pattern: Optional compiled regex for finding the word before
        the cursor to complete. When given, use this regex pattern instead of
        default one (see document._FIND_WORD_RE)
    """

    ##############################################

    def __init__(self, cli, commands: list[str]) -> None:
        self._cli = cli
        self._commands = commands

        self.ignore_case = True
        # self.display_dict = display_dict or {}
        # self.meta_dict = meta_dict or {}
        self.WORD = False
        self.sentence = False
        self.match_middle = False
        self.pattern = None

    ##############################################

    # cf. prompt_toolkit/completion/word_completer.py
    # def _get_completions(
    #         self,
    #         document: Document,
    #         complete_event: CompleteEvent,
    #         words: list[str],
    #         separator: str,
    # ) -> Iterable[Completion]:
    #     # Get list of words.
    #     # if callable(words):
    #     #     words = words()

    #     # Get word/text before cursor.
    #     # if self.sentence:
    #     #     word_before_cursor = document.text_before_cursor
    #     # else:
    #     # word_before_cursor = document.get_word_before_cursor(
    #     #     WORD=self.WORD, pattern=self.pattern
    #     # )
    #     line = document.current_line
    #     index = line.rfind(separator)
    #     word_before_cursor = line[index+1:]

    #     if self.ignore_case:
    #         word_before_cursor = word_before_cursor.lower()

    #     def word_matches(word: str) -> bool:
    #         """True when the word before the cursor matches."""
    #         if self.ignore_case:
    #             word = word.lower()

    #         if self.match_middle:
    #             return word_before_cursor in word
    #         else:
    #             return word.startswith(word_before_cursor)

    #     for _ in words:
    #         if word_matches(_):
    #             # display = self.display_dict.get(_, _)
    #             # display_meta = self.meta_dict.get(_, "")
    #             yield Completion(
    #                 text=_,
    #                 start_position=-len(word_before_cursor),
    #                 # display=display,
    #                 # display_meta=display_meta,
    #             )

    ##############################################

    # def get_completions(
    #         self,
    #         document: Document,
    #         complete_event: CompleteEvent,
    # ) -> Iterable[Completion]:
    #     line = document.current_line.lstrip()
    #     # remove multiple spaces
    #     line = re.sub(' +', ' ', line)
    #     number_of_parameters = line.count(' ')
    #     command = None
    #     right_word = None
    #     parameter_type = None
    #     if number_of_parameters:
    #         # words = [_ for _ in line.split(' ') if _]
    #         # command = words[0]
    #         index = line.rfind(' ')
    #         right_word = line[index+1:]
    #         index = line.find(' ')
    #         command = line[:index]
    #         try:
    #             func = getattr(Cli, command)
    #             signature = inspect.signature(func)
    #             parameters = list(signature.parameters.values())
    #             if len(parameters) > 1:
    #                 parameter = parameters[number_of_parameters]   # 0 is self
    #                 parameter_type = parameter.annotation.__name__   # Fixme: case type alias ???
    #         except AttributeError:
    #             pass
    #     # print(f'Debug: "{command}" | "{right_word}" | {number_of_parameters} | {parameter_type}')

    #     separator = ' '

    #     def handle_cd(current_path, path, folder: bool):
    #         cwd = current_path.find(path)
    #         if '/' in path:
    #             nonlocal separator
    #             separator = '/'
    #         if folder:
    #             return cwd.folder_names
    #         else:
    #             return cwd.leaf_names

    #     if command is None:
    #         words = self._commands
    #     else:
    #         words = ()
    #         match parameter_type:
    #             case 'bool':
    #                 words = ('true', 'false')
    #             case 'CommandName':
    #                 words = self._commands
    #             case 'FilePath':
    #                 # match command:
    #                 #     case 'create' | 'update':
    #                 cwd = Path().cwd()
    #                 filenames = sorted(cwd.glob('*.md'))
    #                 words = [_.name for _ in filenames]
    #             case 'PagePath':
    #                 words = handle_cd(self._cli._current_path, right_word, folder=False)
    #             case 'PageFolder':
    #                 words = handle_cd(self._cli._current_path, right_word, folder=True)
    #             case 'AssetFolder':
    #                 words = handle_cd(self._cli._current_asset_folder, right_word, folder=True)
    #             case 'Tag':
    #                 # Fixme: 'list[Tag]' type is list
    #                 # Fixme: tag can have space !
    #                 words = [_.tag for _ in self._cli._api.tags()]
    #     yield from self._get_completions(document, complete_event, words, separator)

####################################################################################################

class Cli:

    CLI_HISTORY = Path('cli_history')
    HISTORY_JSON = 'history.json'

    STYLE = Style.from_dict({
        # User input (default text)
        # '': '#000000',
        '': '#ffffff',
        # Prompt
        'prompt': '#ff0000',
        # Output
        # 'red': '#ff0000',
        # 'green': '#00ff00',
        # 'blue': '#0000ff',
        'red': '#ed1414',
        'green': '#10cf15',
        'blue': '#1b99f3',
        'orange': '#f57300',
        'violet': '#9b58b5',
        'greenblue': '#19bb9c',
    })

    ##############################################

    def __init__(self, commands_path) -> None:
        self._modules = {}
        self._import_commands(commands_path)
        self._command_map = {}
        self._lookup_commands(self.__class__)
        for _ in CommandGroup.SUBCLASSES:
            self._lookup_commands(_)
        self._commands = sorted(self._command_map.keys())
        self._completer = WordCompleter(self._commands)
        # self._completer = CustomCompleter(self, self.COMMANDS)

    ##############################################

    def _import_commands(self, path: Path):
        name = path.name
        spec = importlib.util.spec_from_file_location(name, path.joinpath('__init__.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._modules[name] = module
        return module

    ##############################################

    def _lookup_commands(self, cls) -> None:
        for _ in dir(cls):
            if not (_.startswith('_') or _[0].isupper() or _ in ('start', 'print')):
                if _ not in self._command_map:
                    self._command_map[_] = getattr(cls, _)
                else:
                    raise NameError(f"Command {_} is already defined")

    ##############################################

    @staticmethod
    def _to_bool(value: str) -> bool:
        if isinstance(value, bool):
            return value
        match str(value).lower():
            case 'true' | 't':
                return True
            case _:
                return False

    ##############################################

    def _print_invalid_command(self, query: str) -> None:
        self.print(f"<red>Invalid command</red> <blue>{query}</blue>")

    ##############################################

    def _process_line(self, query: str) -> bool:
        if '<' in query:
            # Fixme:
            query = query.replace('<', '...')
            self._print_invalid_command(query)
            return True
        # try:
        command, *argument = query.split()
        # except ValueError:
        #     if query.strip() == 'quit':
        #         return False
        # print(f"|{command}|{argument}|")
        try:
            if command == 'quit':
                return False
            method = self._command_map[command]
            try:
                method(self, *argument)
            except RootPermissionRequired as e:
                # self.print('Root privileges are required')
                self.print('<red>' + str(e) + '</red>')
            except AbortAction as e:
                self.print(f"<red>Aborded</red> {e}")
            except ValueError as e:
                self.print(f"<red>{e}</red>")
            except Exception as e:
                print(traceback.format_exc())
                print(e)
        except KeyError:
            self.print(f"<red>Invalid command</red> <blue>{query}</blue>")
            self.usage()
        return True

    ##############################################

    def _process_query(self, query: str) -> bool:
        commands = filter(bool, [_.strip() for _ in query.split(';')])
        for _ in commands:
            if not self._process_line(_):
                return False
        return True

    ##############################################

    def start(self, query: str = '') -> None:
        if query:
            if not self.run(query):
                return

        history = FileHistory(self.CLI_HISTORY)
        session = PromptSession(
            completer=self._completer,
            history=history,
        )
        self.usage()
        while True:
            try:
                message = [
                    ('class:prompt', '> '),
                ]
                query = session.prompt(
                    message,
                    style=self.STYLE,
                )
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            else:
                if query:
                    if not self._process_query(query):
                        break
                else:
                    self.usage()

    ##############################################

    def print(self, message: str = '') -> None:
        if message:
            message = HTML(message)
        print_formatted_text(
            message,
            style=self.STYLE,
        )

    ##############################################

    def clear(self) -> None:
        shortcuts.clear()

    ##############################################

    def usage(self) -> None:
        user = getpass.getuser()
        if user == 'root':
            user_message = 'You are <red>SuperUser</red> !!!'
        else:
            user_message = f'User is <green>{user}</green>'
        for _ in (
            "<red>Enter</red>: <blue>command argument</blue>",
            "    or <blue>command1 argument; command2 argument; ...</blue>",
            "<red>Commands are</red>: " + ', '.join([f"<blue>{_}</blue>" for _ in self._commands]),
            "use <blue>help</blue> <green>command</green> to get help",
            "use <green>tab</green> key to complete",
            "use <green>up/down</green> key to navigate history",
            "<red>Exit</red> using command <blue>quit</blue> or <blue>Ctrl+d</blue>",
            '',
            user_message,
            ''
        ):
            self.print(_)

    ##############################################

    # def _absolut_path(self, path: str) -> PurePosixPath:
    #     if not path.startswith('/') and self._current_path:
    #         path = self._current_path.join(path)
    #     return PurePosixPath(path)

    ##############################################

    def help(self, command: CommandName = '') -> None:
        if not command:
            self.usage()
        else:
            try:
                method = self._command_map[command]
            except KeyError:
                raise AbortAction(f"any {command} command")
            # help(func)
            self.print(f'<blue>{method.__doc__}</blue>')
            signature = inspect.signature(method)
            for _ in signature.parameters.values():
                if _.default != inspect._empty:
                    default = f' = <orange>{_.default}</orange>'
                else:
                    default = ''
                self.print(f'  <blue>{_.name}</blue>: <green>{_.annotation.__name__}</green>{default}')

####################################################################################################

class CommandGroup:
    SUBCLASSES = []

    ##############################################

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.SUBCLASSES.append(cls)
