#!/usr/bin/env python

from __future__ import print_function

import argparse
import re
import sys


IS_PY3 = sys.version_info[0] == 3


def get_args():
    """Parse and return args"""

    parser = argparse.ArgumentParser(
        prog='bump',
        description="Bumps package version numbers")
    parser.add_argument('files', help='Files to update', nargs='+')
    parser.add_argument('-M', dest='number', action='store_const',
                        const='major', help="Bump major number")
    parser.add_argument('-m', dest='number', action='store_const',
                        const='minor', help="Bump minor number")
    parser.add_argument('-b', dest='number', action='store_const',
                        const='build', help="Bump build number")
    parser.add_argument('-s', dest='suffix', type=str,
                        help="Update suffix")

    return parser.parse_args()


def bump_version(version_string, number, suffix):
    """
    Bumps a version number.
    Returns bumped version string or None if version string is invalid.
    """
    match = re.search('([0-9\.]+)([^0-9\.]*)', version_string)
    version_string = match.group(1)
    curr_suffix = match.group(2)
    try:
        version = list(map(int, version_string.split('.')))
    except ValueError:
        pass
    else:
        while len(version) < 3:
            version += [0]
        if number == 'major':
            version = version[0] + 1, 0, 0
        elif number == 'minor':
            version = version[0], version[1] + 1, 0
        elif number == 'build' or suffix is None:
            version = version[0], version[1], version[2] + 1
        if suffix is None:
            suffix = curr_suffix
        return '.'.join(map(str, version)) + suffix


def get_matches(files, number, suffix=None):
    """Returns dict of version definition matches"""

    matches = {}

    for filename in files:
        with open(filename, 'rb') as f:
            match = re.search(
                '\s*[\'"]?version[\'"]?\s*[=:]\s*[\'"]?([^\'",]+)[\'"]?',
                f.read().decode('utf-8'), re.I)

        if match:
            version_string = match.group(1)
            bumped_version_string = bump_version(version_string, number,
                                                 suffix)

            if not bumped_version_string:
                print("Invalid version string in {}: {}"
                      .format(filename, version_string))
                continue

            matches[filename] = dict(
                match=match,
                version_string=version_string,
                bumped_version_string=bumped_version_string)

        else:
            print("No version definition found in", filename)

    return matches


def main():
    matches = get_matches(**get_args().__dict__)

    if len(matches) < 1:
        exit(1)

    # Print bumps
    for filename, match in matches.items():
        print("{}: {} => {}".format(filename, match['version_string'],
                                    match['bumped_version_string']))

    # Confirm update
    __input = input if IS_PY3 else raw_input
    if __input("Is this ok? y/n ").lower() != 'y':
        print("Cancelled")
        exit(1)

    # Update files
    for filename, match in matches.items():
        with open(filename, 'wb') as f:
            bumped_version_string = match['bumped_version_string']
            content = (bytes(match['match'].string, 'utf-8') if IS_PY3 else
                       match['match'].string)
            if IS_PY3:
                bumped_version_string = bytes(bumped_version_string, 'utf-8')
            f.write(content[:match['match'].start(1)] +
                    bumped_version_string + content[match['match'].end(1):])
            print("Updated", filename)


if __name__ == '__main__':
    main()
