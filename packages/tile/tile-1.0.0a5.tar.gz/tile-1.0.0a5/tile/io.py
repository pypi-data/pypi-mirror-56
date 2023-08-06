import collections
import re

from typing import Iterator, TextIO

from .constants import TILE_END, TILE_START, TILE_WARNING


def from_file(file: TextIO) -> Iterator[str]:
    with file as f:
        yield from f


def to_file(file: TextIO, lines: Iterator[str]):
    with file as f:
        f.write("\n".join(lines))


def to_nowhere(lines: Iterator[str]):
    collections.deque(lines, 0)


def to_config(config_file: TextIO, lines: Iterator[str]):
    with config_file as f:
        text = f.read()
        f.seek(0)
        f.truncate()
        text = re.sub(fr"^{TILE_START}\n.*{TILE_END}\n?", r"", text, flags=re.MULTILINE | re.DOTALL)
        f.write("\n".join((text.strip(), TILE_START, TILE_WARNING, *lines, TILE_END)))
