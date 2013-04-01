import argparse
import re


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
        m = re.search('\s*version\s*=\s*(\'|")?([^\'",]+)(\'|")?', f.read(),
                      re.I)
    if m:
        version_string = m.group(2)
        try:
            version = map(int, version_string.split('.'))
        except ValueError:
            print "Invalid version string:", version_string
        while len(version) < 3:
            version += [0]
        if args.major:
            version = version[0] + 1, 0, 0
        elif args.minor and len(version) > 1:
            version = version[0], version[1] + 1, 0
        elif len(version) > 2:
            version = version[0], version[1], version[2] + 1
        else:
            print "Invalid version string:", version_string
        new_version_string = '.'.join([str(c) for c in version])
        print version_string, '=>', new_version_string

        if raw_input('Is this ok? y/n ').lower() == 'y':
            with open(args.file, 'wb') as f:
                f.write(m.string[:m.start(2)] + '.'.join(map(str, version)) +
                        m.string[m.end(2):])
            print 'Updated', args.file
        else:
            print 'Canceled'

    else:
        print "No version definition found"


if __name__ == '__main__':
    main()
