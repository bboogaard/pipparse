import subprocess
import sys

from semantic_version import Version


VERSION_MAJOR = 'major'
VERSION_MINOR = 'minor'
VERSION_PATCH = 'patch'

VERSIONS = (VERSION_PATCH, VERSION_MINOR, VERSION_MAJOR)


def get_numeric_version(version: str) -> int:
    try:
        return VERSIONS.index(version)
    except ValueError:
        return -1


def check():
    return subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated"]).decode()


def parse(output: str, version_filter: str):

    def parse_columns(ln):
        ln = ln.lstrip()
        cols = []
        col = ''
        for pos, char in enumerate(ln):
            col += char.strip()
            if (char == ' ' or pos == len(ln) - 1) and col:
                cols.append(col)
                col = ''
        return cols

    lines = list(filter(lambda l: l.strip() != '', output.split('\n')))
    new_lines = []
    for line in lines:
        columns = parse_columns(line)
        try:
            version = Version(columns[1])
            latest = Version(columns[2])
        except ValueError:
            new_lines.append(line)
            continue

        if latest.major > version.major:
            update = get_numeric_version(VERSION_MAJOR)
        elif latest.minor > version.minor:
            update = get_numeric_version(VERSION_MINOR)
        else:
            update = get_numeric_version(VERSION_PATCH)

        if get_numeric_version(version_filter) >= update:
            new_lines.append(line)

    return '\n'.join(new_lines)


def run():
    try:
        version_filter = sys.argv[1]
        print(parse(check(), version_filter))
    except IndexError:
        print("Please parse version filter as positional argument")
