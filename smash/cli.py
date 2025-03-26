import argparse
import sys
from .commands import run_init, run_build


def main():
    parser = argparse.ArgumentParser(
        prog="smash", description="Smash – build system for content"
    )
    parser.add_argument("--version", action="version", version="Smash 0.1.0")
    parser.add_argument("command", nargs="?", help="Command to run (e.g., init, build)")

    args = parser.parse_args()

    if args.command == "init":
        run_init()
    elif args.command:
        print(f"Unknown command: {args.command}")
        sys.exit(1)
    else:
        run_build()
