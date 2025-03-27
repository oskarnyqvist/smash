## 12. [Story] smash add: Create a new smashlet

Description
As a developer, I want to scaffold a new smashlet\_<name>.py file using a CLI command, so I can get started quickly without copy-pasting boilerplate.

Acceptance Criteria

smash add <name> creates a file like smashlet\_<name>.py in the current directory.

The file includes boilerplate: INPUT_GLOB, OUTPUT_DIR, and a stub run() function.

Optional flags for:

--glob "\*.md"

--output "dist/"

--context (if the user wants to pass context)

Prevents overwriting existing files.

Verification

Run smash add render → file created with expected contents.

Confirm contents and structure match expectations.
