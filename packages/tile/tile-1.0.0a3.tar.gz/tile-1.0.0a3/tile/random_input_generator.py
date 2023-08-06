import random
import string
import sys

from .io import to_nowhere
from .tree_algorithms import parse


def generate_line():
    length = random.randrange(200)
    return "".join(random.choices(string.printable, k=length))


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        lines = int(sys.argv[1])
    else:
        lines = 1000

    try:
        to_nowhere(parse((generate_line() for x in range(lines)), strict=True))
    except:
        print("FAIL")
