import click
import re

VALID_TEXT = re.compile('^[0-9A-Za-z\-\.]$')


class SemVer(object):

  __slots__ = [
    'major',
    'minor',
    'patch',
    'pre',
    'build',
  ]

  def __init__(self, **kwargs):
    for n in self.__slots__:
      setattr(self, n, kwargs.get(n))

  def __repr__(self):
    return "<SemVer {}>".format(
      ", ".join([
        "{}={}".format(n, getattr(self, n))
        for n in self.__slots__
      ]))

  def __str__(self):
    version_string = ".".join(map(str,
      [self.major, self.minor, self.patch]))
    if self.pre:
      version_string += "-" + self.pre
    if self.build:
      version_string += "+" + self.build
    return version_string

  @classmethod
  def parse(cls, version):
    major = minor = patch = 0
    build = pre = None
    build_split = version.split('+')
    if len(build_split) > 1:
      version, build = build_split
    pre_split = version.split('-', 1)
    if len(pre_split) > 1:
      version, pre = pre_split
    major_split = version.split('.', 1)
    if len(major_split) > 1:
      major, version = major_split
      minor_split = version.split(b'.', 1)
      if len(minor_split) > 1:
        minor, version = minor_split
        if version:
          patch = version
      else:
        minor = version
    else:
      major = version
    return cls(
      major=int(major),
      minor=int(minor),
      patch=int(patch),
      pre=pre,
      build=build,
    )

  def bump(self, **kwargs):
    number = kwargs.get('number')
    if number == 'major':
      self.major += 1
    elif number == 'minor':
      self.minor += 1
    elif number == 'patch':
      self.patch += 1
    self.pre = kwargs.get('pre')
    self.build = kwargs.get('build')


@click.command()
@click.option('--major', '-M', 'number', flag_value='major',
              help="Bump major number")
@click.option('--minor', '-m', 'number', flag_value='minor',
              help="Bump minor number")
@click.option('--patch', '-p', 'number', flag_value='patch',
              help="Bump patch number")
@click.option('--pre', help="Set pre-release identifier")
@click.option('--build', help="Set build metadata")
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def main(**kwargs):
  version_string = kwargs['input'].read()
  version = SemVer.parse(version_string)
  version.bump(**kwargs)
  click.echo(version)


if __name__ == '__main__':
  main()
