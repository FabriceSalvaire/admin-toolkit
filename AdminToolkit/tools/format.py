####################################################################################################

__all__ = ['byte_humanize', 'ibyte_humanize']

####################################################################################################

import os

####################################################################################################

LINESEP = os.linesep

####################################################################################################

def fix_none(value):
    if value is None:
        return ''
    return value

####################################################################################################

def _humanize(size: int, binary: bool = False, number_of_digits: int = 1) -> str:
    if not size:
        return None
    BASE = 1024 if binary else 1000
    I_PREFIX = 'i' if binary else ''
    PREFIXES = ('', 'k', 'M', 'G', 'T', 'P')
    ZERO = '.' + '0'*number_of_digits
    for prefix in PREFIXES:
        _ = size / BASE
        if int(_) == 0:
            size = str(round(size, number_of_digits))
            if size.endswith(ZERO):
                size = size[:-len(ZERO)]
            return f'{size}{prefix}{I_PREFIX}B'
        else:
            size = _

def byte_humanize(size: int) -> str:
    return _humanize(size)

def ibyte_humanize(size: int) -> str:
    return _humanize(size, binary=True)

####################################################################################################

class Table:

    ##############################################

    def __init__(self, format: dict, header: dict, sep: str = ' | ') -> None:
        self._format = {key: str(value) for key, value in format.items()}
        self._header = {key: str(value) for key, value in header.items()}
        self._number_of_columns = len(self._format.keys())
        self._sep = str(sep)
        self._lines = []

    ##############################################

    def append(self, **kwargs) -> None:
        self._lines.append(kwargs)
        # len1 = self._number_of_columns
        # # if len1 is not None:
        # len2 = len(kwargs.keys())
        # if len1 != len2:
        #     raise ValueError(f'number of columns mismatch {len1} vs {len2}')
        # if self.number_of_columns is None:
        #     self._number_of_columns = len(self._lines[0])

    ##############################################

    def __str__(self) -> str:
        def colored_len(text: str) -> int:
            # return len(text)
            l = 0
            in_color = False
            for c in text:
                if in_color:
                    if c == '>':
                        in_color = False
                else:
                    if c == '<':
                        in_color = True
                    else:
                        l += 1
            return l

        lengths = {column: len(self._header[column]) for column in self._format.keys()}
        formated_lines = []
        for line in self._lines:
            formated_line = []
            for column in self._format.keys():
                formated_value = ''
                if column in line:
                    value = line[column]
                    if value:
                        format_str = self._format[column]
                        formated_value = format_str.format(value)
                formated_line.append(formated_value)
                lengths[column] = max(lengths[column], colored_len(formated_value))
            formated_lines.append(formated_line)
        text = ''
        columns = []
        for column, value in self._header.items():
            format_str = '{:^%s}' % (lengths[column])
            columns.append(format_str.format(value))
        text += self._sep.join(columns) + LINESEP
        for line in formated_lines:
            columns = []
            for column, value in zip(self._format.keys(), line):
                format_str = self._format[column]
                padding = lengths[column] - colored_len(value)
                if ':^' in format_str:
                    left = padding // 2
                    _ = ' '*left + value + ' '*(padding - left)
                if ':>' in format_str:
                    _ = ' '*padding + value
                else:
                     _ = value + ' '*padding
                columns.append(_)
            text += self._sep.join(columns) + LINESEP
        return text
