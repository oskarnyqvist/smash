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

    add_parser = subparsers.add_parser("add", help="Create a new smashlet_<name>.py")
    add_parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Optional name for the smashlet (e.g., 'render'). If omitted, creates 'smashlet.py'.",
    )
    add_parser.add_argument(
        "--glob", default="*", help="Input glob pattern (default: '*')"
    )
    add_parser.add_argument(
        "--output", default="dist/", help="Output directory (default: 'dist/')"
    )
    add_parser.add_argument(
        "--context", action="store_true", help="Use run(context) instead of run()"
    )

    args = parser.parse_args()

    if args.command == "init":
        run_init()
    elif args.command == "build" or args.command is None:
        run_build()
    elif args.command == "add":
        from .commands import run_add_smashlet

        run_add_smashlet(
            name=args.name,
            glob=args.glob,
            output=args.output,
            context_mode=args.context,
        )
    else:
        parser.print_help()
