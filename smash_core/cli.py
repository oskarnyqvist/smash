# cli.py
#
# Smash CLI entry point.
# Dispatches commands for init, build, add, and run (force) using the refactored modules.

import argparse

# Import commands from refactored modules
from smash_core.commands import run_init
from smash_core.commands import run_build, run_force
from smash_core.commands import run_add_smashlet


def main():
    """
    Smash CLI dispatcher.

    Usage:
      smash init           → Initialize a new Smash project
      smash build          → Run the build process (default if no command)
      smash --version      → Show version info
      smash add [options]  → Create a new smashlet file with boilerplate
      smash run [path]     → Force-run a specific smashlet or all
    """
    parser = argparse.ArgumentParser(
        prog="smash", description="Smash – build system for content"
    )
    parser.add_argument("--version", action="version", version="Smash 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    # Init command
    subparsers.add_parser("init", help="Initialize a new Smash project")

    # Build command
    subparsers.add_parser("build", help="Run the build process")

    # Add command
    add_parser = subparsers.add_parser(
        "add", help="Create a new smashlet with boilerplate"
    )
    add_parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Optional name for the smashlet (e.g., 'render'). If omitted, uses default filename from template.",
    )
    add_parser.add_argument(
        "--template",
        default="default",
        help="Template to use for the smashlet (default: 'default'). Options: default, minimal, pandas",
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

    # Run command for force-running smashlets
    run_parser = subparsers.add_parser(
        "run", help="Force run smashlets, bypassing skip logic"
    )
    run_parser.add_argument(
        "smashlet_path",
        nargs="?",
        help="Optional path to a specific smashlet to force-run",
    )

    args = parser.parse_args()

    if args.command == "init":
        run_init()
    elif args.command == "build" or args.command is None:
        run_build()
    elif args.command == "add":
        run_add_smashlet(
            name=args.name,
            template=args.template,
            glob=args.glob,
            output=args.output,
            context_mode=args.context,
        )
    elif args.command == "run":
        run_force(args.smashlet_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
