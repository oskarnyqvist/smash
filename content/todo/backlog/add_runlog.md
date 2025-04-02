### 🆕 TASK: Add detailed per-smashlet runlog metadata

Extend `.smash/runlog.json` to store:

- `last_run`: last successful run (timestamp)
- `last_skip`: last skip (timestamp)
- `runs`: total number of times run

Fallback: if value is a float, treat it as `last_run` (legacy support).

Update logic:

- On run: set `last_run`, increment `runs`
- On skip: update `last_skip`

Add tests for:

- structured runlog entries
- legacy fallback
- skip vs run behavior

Enables richer `smash status`, debugging, and future metrics.
