# cli.py
#
# Smash CLI entry point using subcommands.
# Handles top-level project actions like `init` and `build`.

import argparse
from .commands import run_init, run_build


def main():
    """
    Smash CLI dispatcher.

    Usage:
      smash init        → Create a new .smash/ directory
      smash build       → Run the build loop (default if no command)
      smash --version   → Show version info
    """
    parser = argparse.ArgumentParser(
        prog="smash", description="Smash – build system for content"
    )
    parser.add_argument("--version", action="version", version="Smash 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize a new Smash project")
    subparsers.add_parser("build", help="Run the build process")

    args = parser.parse_args()

    if args.command == "init":
        run_init()
    elif args.command == "build" or args.command is None:
        run_build()
    else:
        parser.print_help()
