# Smash

Smash is a lightweight build system for content.

It lets you define, in plain Python, how files in a directory should be transformed — without global config, dependency graphs, or special formats.

Each directory contains its own `smashlet_*.py` files. These scripts declare what files to process and how. Smash runs them in order, automatically and predictably.

Built for developers who want local-first, scriptable workflows — not orchestration platforms or site engines.
