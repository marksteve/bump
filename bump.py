#!/usr/bin/env python

from __future__ import print_function

import argparse
import re
import sys


IS_PY3 = sys.version_info[0] == 3


def main():
    parser = argparse.ArgumentParser(
        prog='bump',
        description="Bumps package version numbers")
    parser.add_argument('files', help='Files to update', nargs='+')
    parser.add_argument('-M', dest='major', action='store_true', default=False,
                        help="Bump major version")
    parser.add_argument('-m', dest='minor', action='store_true', default=False,
                        help="Bump minor version")
    parser.add_argument('-b', dest='build', action='store_true', default=True,
                        help="Bump build version")
    args = parser.parse_args()

    matches = {}

    for filename in args.files:

        with open(filename, 'rb') as f:
            match = re.search(
                '\s*[\'"]?version[\'"]?\s*[=:]\s*[\'"]?([^\'",]+)[\'"]?',
                f.read().decode('utf-8'), re.I)

        if match:
            version_string = match.group(1)
            try:
                version = list(map(int, version_string.split('.')))
            except ValueError:
                print("Invalid version string in", filename, ":",
                      version_string)
            else:
                while len(version) < 3:
                    version += [0]
                if args.major:
                    version = version[0] + 1, 0, 0
                elif args.minor:
                    version = version[0], version[1] + 1, 0
                elif args.build:
                    version = version[0], version[1], version[2] + 1

                new_version_string = '.'.join(map(str, version))

                matches[filename] = dict(match=match,
                                         version_string=version_string,
                                         new_version_string=new_version_string)

        else:
            print("No version definition found in", filename)

    if len(matches) < 1:
        print("No files to update")
        exit(1)

    for filename, match in matches.items():
        print(filename, ':', match['version_string'], '=>',
              match['new_version_string'])

    __input = input if IS_PY3 else raw_input

    if __input('Is this ok? y/n ').lower() == 'y':
        for filename, match in matches.items():
            new_version_string = match['new_version_string']
            with open(filename, 'wb') as f:
                content = (bytes(match['match'].string, 'utf-8') if IS_PY3 else
                           match['match'].string)
                if IS_PY3:
                    new_version_string = bytes(new_version_string, 'utf-8')
                f.write(content[:match['match'].start(1)] +
                        new_version_string + content[match['match'].end(1):])
                print('Updated', filename)
    else:
        print('Cancelled')
        exit(1)


if __name__ == '__main__':
    main()
