####################################################################################################

"""locate interface

"""

####################################################################################################

import subprocess

####################################################################################################

LOCATE = '/usr/bin/plocate'

def locate(pattern: str, basename: bool = False) -> list[str]:
    # Usage: plocate [OPTION]... PATTERN...
    #
    # -b, --basename         search only the file name portion of path names
    # -c, --count            print number of matches instead of the matches
    # -d, --database DBPATH  search for files in DBPATH
    #                         (default is /var/lib/plocate/plocate.db)
    # -i, --ignore-case      search case-insensitively
    # -l, --limit LIMIT      stop after LIMIT matches
    # -0, --null             delimit matches by NUL instead of newline
    # -N, --literal          do not quote filenames, even if printing to a tty
    # -r, --regexp           interpret patterns as basic regexps (slow)
    #     --regex            interpret patterns as extended regexps (slow)
    # -w, --wholename        search the entire path name (default; see -b)
    #     --help             print this help
    #     --version          print version information

    # -b, --basename
    # Match  only against the file name portion of the path name, ie., the directory names will be excluded from the
    # match (but still printed). This does not speed up the search, but can suppress uninteresting matches.
    #
    # -c, --count
    # Do not print each match. Instead, count them, and print out a total number at the end.
    #
    # -d, --database DBPATH
    # Find matches in the given database, instead of /var/lib/plocate/plocate.db.  This argument can be given multi‐
    # ple times, to search multiple databases.  It is also possible to give multiple databases in one argument, sep‐
    # arated by :.  (Any character, including : and \, can be escaped by prepending a \.)
    #
    # -e, --existing
    # Print only entries that refer to files existing at the time locate is run. Note that unlike  mlocate(1),  sym‐
    # links are not followed by default (and indeed, there is no option to change this).
    #
    # -i, --ignore-case
    # Do  a  case-insensitive  match as given by the current locale (default is case-sensitive, byte-by-byte match).
    # Note that plocate does not support the full range of Unicode case folding rules; in particular, searching  for
    # ß will not give you matches on ss even in a German locale. Also note that this option will be somewhat slower
    # than a case-sensitive match, since it needs to generate more candidates for searching the index.
    #
    # -l, --limit LIMIT
    # Stop searching after LIMIT matches have been found. If --count is given, the number printed  out  will  be  at
    # most LIMIT.
    #
    # -N, --literal
    # Print entry names without quoting. Normally, plocate will escape special characters in filenames, so that they
    # are  safe  for consumption by typical shells (similar to the GNU coreutils shell-escape-always quoting style),
    # unless printing to a pipe, but this options will turn off such quoting.
    #
    # -0, --null
    # Instead of writing a newline after every match, write a NUL (ASCII 0). This is useful for creating unambiguous
    # output when it is to be processed by other tools (like xargs(1)), as filenames are allowed to contain embedded
    # newlines.
    #
    # -r, --regexp
    # Patterns are taken to be POSIX basic regular expressions.  See regex(7) for more information.
    # Note that this forces a linear scan through the entire database, which is slow.
    #
    # --regex
    # Like --regexp, but patterns are instead taken to be POSIX extended regular expressions.
    #
    # -w, --wholename
    # Match against the entire path name. This is the default, so unless -b is given first (see above), it will not
    # do anything. This option thus exists only as compatibility with mlocate(1).

    cmd = (
        LOCATE,
        '--basename',
        # '-r',
        # f'^{pattern}$',
        pattern,
    )
    print(cmd)
    process = subprocess.run(cmd, capture_output=True)
    return process.stdout.decode('utf8').splitlines()
