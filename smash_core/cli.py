# cli.py

"""
Command-line entry point for Smash.

Parses arguments and dispatches to subcommands like `init`, `build`, `add`, `run`, and `status`.
This is the main script run when you type `smash` in the terminal.
"""

import argparse
from smash_core.commands import run_init, run_build, run_force, run_add_smashlet
from smash_core.commands.status import run_status


def main():
    """
    Smash CLI dispatcher.

    Commands:
      smash init         → Initialize a new Smash project
      smash build        → Run the build process (default)
      smash add [...]    → Create a new smashlet file
      smash run [...]    → Force-run smashlets
      smash status       → Show which smashlets would run (dry-run)
    """
    parser = argparse.ArgumentParser(
        prog="smash", description="Smash – build system for content"
    )
    parser.add_argument("--version", action="version", version="Smash 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize a new Smash project")
    subparsers.add_parser("build", help="Run the build process")

    add_parser = subparsers.add_parser("add", help="Create a new smashlet")
    add_parser.add_argument("name", nargs="?", default=None)
    add_parser.add_argument("--template", default="default")
    add_parser.add_argument("--glob", default="*", help="Input glob pattern")
    add_parser.add_argument("--output", default="dist/", help="Output directory")
    add_parser.add_argument("--context", action="store_true", help="Use run(context)")

    run_parser = subparsers.add_parser("run", help="Force run smashlets")
    run_parser.add_argument("smashlet_path", nargs="?")

    subparsers.add_parser("status", help="Show smashlet run status (dry run)")

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
    elif args.command == "status":
        run_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
