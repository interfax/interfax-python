#!/usr/bin/env python
import os
import re
import subprocess
import sys
from datetime import date, datetime

RE_CHANGES = r'^(Version (.*))\n(-*)\n\n+Released on (\d{4}-\d{2}-\d{2})$'
RE_VERSION = r"(__version__\s+=\s)'.*'"


def run(*args):
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def set_version(version):
    with open('interfax/__init__.py') as f:
        content = f.read()

    output = re.sub(RE_VERSION, r"\1'{}'".format(version), content)

    if content != output:
        with open('interfax/__init__.py', 'w') as f:
            f.write(output)


def increment_version(version):
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    version = None
    release_date = None

    with open('CHANGES') as f:
        for match in re.finditer(RE_CHANGES, f.read(1024), re.M):

            if len(match.group(1)) != len(match.group(3)):
                continue

            version = match.group(2)
            release_date = datetime.strptime(match.group(4), '%Y-%m-%d').date()
            break

    tag = 'v{}'.format(version)

    if version is None:
        print('error: cannot read CHANGES')
        exit(1)

    if release_date != date.today():
        print('error: release date is not today')
        exit(1)

    tags = set(run('git', 'tag').communicate()[0].decode('utf-8').splitlines())

    if tag in tags:
        print('error: tag {} already exists'.format(tag))
        exit(1)

    if run('git', 'diff', '--quiet').wait() != 0:
        print('error: git repo not clean')
        exit(1)

    set_version(version)
    run('git', 'commit', '-am', 'Version {}'.format(version)).wait()
    run('git', 'tag', '-am', 'Version {}'.format(version), tag).wait()
    run(sys.executable, 'setup.py', 'sdist', 'upload').wait()
    run(sys.executable, 'setup.py', 'bdist_wheel', 'upload').wait()
    set_version(increment_version(version) + '-dev')


if __name__ == '__main__':
    main()
