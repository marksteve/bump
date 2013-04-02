from __future__ import print_function

import argparse
import re
import sys


IS_PY3 = sys.version_info[0] == 3


def main():
    parser = argparse.ArgumentParser(
        prog='bump',
        description="Bumps package version numbers")
    parser.add_argument('file', help='File to update')
    parser.add_argument('-M', dest='major', action='store_true',
                        help="Bump major version")
    parser.add_argument('-m', dest='minor', action='store_true',
                        help="Bump minor version")
    parser.add_argument('-b', dest='build', action='store_true',
                        help="Bump build version")
    args = parser.parse_args()

    with open(args.file, 'rb') as f:
        m = re.search('\s*[\'"]?version[\'"]?\s*[=:]\s*[\'"]?([^\'",]+)[\'"]?',
                      f.read().decode('utf-8'), re.I)

    if m:
        version_string = m.group(1)
        try:
            version = list(map(int, version_string.split('.')))
        except ValueError:
            print("Invalid version string:", version_string)
        while len(version) < 3:
            version += [0]
        if args.major:
            version = version[0] + 1, 0, 0
        elif args.minor:
            version = version[0], version[1] + 1, 0
        else:
            version = version[0], version[1], version[2] + 1

        new_version_string = '.'.join(map(str, version))
        print(version_string, '=>', new_version_string)

        __input = input if IS_PY3 else raw_input

        if __input('Is this ok? y/n ').lower() == 'y':
            with open(args.file, 'wb') as f:
                content = bytes(m.string, 'utf-8') if IS_PY3 else m.string
                if IS_PY3:
                    new_version_string = bytes(new_version_string, 'utf-8')
                f.write(content[:m.start(1)] + new_version_string +
                        content[m.end(1):])
                print('Updated', args.file)
        else:
            print('Canceled')

    else:
        print("No version definition found")


if __name__ == '__main__':
    main()
