"""
`clide update` automatically searches for any clide scripts in the current source repository and updates them
"""
import os
import re
import shlex
import shutil
import subprocess
import sys
import urllib.request
from typing import Dict, Iterator
from pathlib import Path

from .atomic_write import atomic_write_context

RE_PREFIX = re.compile(r"^\s*")
RE_SETTING = re.compile(r"^([a-z]+): ([^ ]+)$")


def abort(message: str):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def warning(message: str):
    print(f"Warning: {message}", file=sys.stderr)


def _decode_settings(lines: Iterator[str]):
    """
    Decodes an extremely limited YAML subset
    """
    prefix = None
    rv = {}
    for line in lines:
        line_prefix = RE_PREFIX.match(line).group(0)

        # Grab the first prefix we see, and exit if we ever see less
        if prefix is None:
            prefix = line_prefix
        elif len(line_prefix) < len(prefix):
            return rv

        line = line[len(prefix) :]
        match = RE_SETTING.match(line)
        if not match:
            warning("Unhandled clide settings line: %s" % repr(line))
            continue

        (setting, value) = match.groups()
        rv[setting] = value
    return rv


def _decode_config(lines: Iterator[str], prefix: str):
    yaml = []
    for line in lines:
        if line.startswith(prefix):
            yaml.append(line[len(prefix) :].rstrip())
        else:
            break
    return _decode_settings(yaml)


def read_clide_configuration(path: Path):
    with open(path, "r") as f:
        lines = iter(f)
        for line in lines:
            if not line.startswith("#"):
                return None
            if line.rstrip() == "# clide:":
                # decode configuration requiring atleast one space more
                # this could be vastly improved later
                return _decode_config(lines, "#  ")


def fetch_latest(path: Path, config: Dict[str, str]):
    with urllib.request.urlopen(config["source"]) as response:
        with atomic_write_context(path, "w+b") as f:
            shutil.copyfileobj(response, f)


def update():
    # In future we may want to support more version control systems
    if not shutil.which("git"):
        abort("`clide update` requires a git client")
        print()

    try:
        file_list = subprocess.check_output(["git", "ls-files"], encoding="utf-8")
    except subprocess.CalledProcessError:
        abort("Listing files (`git ls-files`) failed.")

    for path in (Path(path) for path in shlex.split(file_list)):
        config = read_clide_configuration(path)
        if config:
            fetch_latest(path, config)


if __name__ == "__main__":
    update()
