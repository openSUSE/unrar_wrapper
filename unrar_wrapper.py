#!/usr/bin/python3

"""
UnRAR wrapper is a wrapper python script that transforms the basic UnRAR
commands to unar and lsar calling in order to provide a backwards
compatibility.
It supports only a subset of the UnRAR commands and options:
Supported commands: l[t[a],b], t, v[t[a],b], x.
Supported options: -o+, -o-, -or, -p
Other: files, @listfiles and path_to_extract (only for unar)
Return codes: 0 (success), 1 (error), 2 (invalid argument)
"""

import argparse
import subprocess
import sys


def parse_args():
    """Create a parser and parse UnRAR synopsis.

    The UnRAR synopsis is as follows:
      unrar command [option1] [optionN] archive [files...] [@list-files...]
      [path_to_extract/]
    Support the following commands: l[t[a],b], t, v[t[a],b], x.
    Support the following options: -o+, -o-, -or, -p

    Args:
    Returns:
        A namespace class that holds parsed arguments
    Raises:
    """

    parser = argparse.ArgumentParser(description="Transforms the basic UnRAR "
                                                 "commands to unar and lsar "
                                                 "calling in order to provide "
                                                 "a backwards compatibility")
    parser.add_argument('command',
                        choices=['l', 'lt', 'lta', 'lb', 't', 'v', 'vt',
                                 'vta', 'vb', 'x'],
                        help="UnRAR command")
    parser.add_argument('-o',
                        dest='overwrite',
                        choices=['+', '-', 'r'],
                        help="'-o+' Set the overwrite mode, '-o-' Unset the "
                             "overwrite mode,'-or' Rename files automatically")
    parser.add_argument('-p',
                        dest='password',
                        help='-p[password] Set password.')
    parser.add_argument('archive',
                        help='The path to the archive')
    parser.add_argument('rest',
                        nargs='*',
                        help="[files...] [@list-files...] [path_to_extract/]")

    args = parser.parse_args()
    return args


def transform_syntax(args):
    """Transform UnRAR command and options to the Unarchiver syntax.

    Args:
        args: A namespace class that holds parsed UnRAR arguments
    Returns:
        A tuple (commands, options) with a string and a list that hold
        Unarchiver command and options
    Raises:
    """

    opts = []

    if args.command == 'x':
        command = 'unar'
        # '-o+' means force-overwrite
        if args.overwrite == '+':
            opts.append('-f')
        # '-o-' means force-skip
        elif args.overwrite == '-':
            opts.append('-s')
        # '-or' means force-rename
        elif args.overwrite == 'r':
            opts.append('-r')
    else:
        command = 'lsar'
        if (args.command == 'lb' or
                args.command == 'vb'):
            # 'lb' and 'vb'are translated to plain 'lsar' command
            pass
        elif (args.command == 'l' or
              args.command == 'v'):
            opts.append('-l')
        elif (args.command == 'lt' or
              args.command == 'lta' or
              args.command == 'vt' or
              args.command == 'vta'):
            opts.append('-L')
        elif args.command == 't':
            opts.append('-t')

    # '-p' option makes sense for all commands
    if args.password:
        opts.append('-p')
        opts.append(args.password)

    return command, opts


def transform_list_files(list_files):
    """Return the content of the files given as a list.

    If any of the files doesn't exist then the program is terminated.

    Args:
        list_files: a list of paths to the files
    Returns:
        A list of concatenated content of the files given as list_files
    Raises:
    """

    files = []

    for f in list_files:
        try:
            with open(f, "r") as stream:
                for line in stream:
                    # Remove trailing newline
                    files.append(line.rstrip())
        except IOError:
            print("Cannot open {}\nNo such file or directory".format(f),
                  file=sys.stderr)
            sys.exit(1)

    return files


def process_rest(rest):
    """Split the argument to [files], [@list-files] and [path_to_extract/].

    All of these parts are optional.

    Args:
        rest: a list of strings with the paths to files, @list-files and
        path_to_extract/
    Returns:
        A tuple (files, list_files, path)
        - files: a list of files, that should be processed
        - @list-files: a list of text files that contain a list of files that
          should be processed
        - path_to_extract/: a string with a directory to write the contents of
          the archive to
    Raises:
    """

    if not rest:
        return None, None, None

    # UnRAR considers every item ending with '/' as a path.
    # If multiple paths are present, only the last one is used.
    files = []
    list_files = []
    path = None
    for item in rest:
        if item.endswith('/'):
            path = item
        elif item.startswith('@'):
            list_files.append(item[1:])
        else:
            files.append(item)

    return files, list_files, path


def main():

    args = parse_args()

    # Translate UnRAR command and options to the Unarchiver syntax
    command, options = transform_syntax(args)

    files = []
    if args.rest and command == 'lsar':
        # files, @list_files and path are not supported for lsar
        print("Warning: [files...], [@list_files...] and [path_to_extract/]"
              " are not supported for listing and testing. These parameters"
              " are ignored.", file=sys.stderr)

    if command == 'unar':
        # Add '-D' option by default in order to simulate default UnRAR
        # behaviour (never create a new containing directory if there is more
        # than one top-level file or folder)
        options.append("-D")

        if args.rest:
            files, list_files, path = process_rest(args.rest)

            # unar can't process @list_files as is -> transform it to files
            if list_files:
                files = files + transform_list_files(list_files)

            # Transform path to unar syntax ("-o DIRECTORY")
            if path:
                options.extend(["-o", path])

    # Call Unarchiver
    rc = subprocess.call([command] + options + [args.archive] + files)

    return rc


if __name__ == "__main__":
    return_code = main()
    sys.exit(return_code)
