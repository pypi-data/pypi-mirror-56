import argparse
import pathlib
import sys

from . import __version__
from .io import from_file, to_config, to_file
from .tree_algorithms import parse


def main():
    parser = argparse.ArgumentParser(epilog="Documentation: https://github.com/ViliamV/tile")
    parser.add_argument(
        "infile",
        metavar="input_file",
        type=argparse.FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="if not provided, defaults to stdin",
    )
    parser.add_argument(
        "--config",
        metavar="config_path",
        type=argparse.FileType("r+"),
        help="overwrite config path, only applicable with '--write'",
    )
    parser.add_argument(
        "--sway", action="store_true", help="don't use '--no-startup-id', use sway config file if '--write'",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--write", action="store_true", help="write output directly to i3 config file")
    output_group.add_argument(
        "--output",
        dest="outfile",
        metavar="output_file",
        type=argparse.FileType("w"),
        help="defaults to print to stdout",
        default=sys.stdout,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()
    if args.infile is sys.stdin:
        print("[Interactive mode] Use Ctrl+D to exit")
    if args.write:
        if args.config:
            config = args.config
        else:
            config_path = pathlib.Path.home() / f".config/{'sway' if args.sway else 'i3'}/config"
            if not config_path.is_file():
                print(f"tile: error: No such file: '{config_path}'")
                print("hint: add option '--config config_path'")
                sys.exit(1)
            config = config_path.open("r+")
        to_config(config, parse(from_file(args.infile), sway=args.sway))
    else:
        to_file(args.outfile, parse(from_file(args.infile), sway=args.sway))
