## 🥇 Top Priority: Core Stability & Runtime Correctness

These should likely be tackled first. They fix **real problems** or unlock meaningful behavior:

| Task                             | Why                                                             |
| -------------------------------- | --------------------------------------------------------------- |
| ✅ `add_context_file_support.md` | Fundamental to enabling structured, local context.              |
| ✅ `context_folder_support.md`   | Necessary to align context with locality principle.             |
| ✅ `inject_inputs_in_context.md` | Reduces boilerplate; complements above.                         |
| ✅ `tests_cli.md`                | Ensures all the above changes are safe and prevent regressions. |

> 🔁 These all touch or improve core Smash behavior. Start here.

---

## 🥈 Second Tier: Dev + CLI Ergonomics

These improve usability, feedback loops, or debugging clarity — great follow-ups once the core is solid.

| Task                                                      | Why                                                                          |
| --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| ✅ `add_run_command_for_force.md`                         | Enables debugging and manual control.                                        |
| ✅ `status_command.md`                                    | Lets you inspect what will run and why.                                      |
| ✅ `runlog_viewer_command.md`                             | Useful for understanding build history and skip logic.                       |
| ✅ `centralized_logging.md` + `replace_print_with_log.md` | Clean separation of logic and output — good for future formats or CLI flags. |

> 🔧 Once runtime correctness is in place, these enhance DX and confidence.

---

## 🧠 Third Tier: Docs & LLM Support

These are important, but not blockers — they **amplify understanding**, not correctness:

| Task                                 | Why                                                           |
| ------------------------------------ | ------------------------------------------------------------- |
| ✅ `generate_context_docs.md`        | Clarifies core concept — should follow context support.       |
| ✅ `generate_file_overview.md`       | Helps humans + LLMs discover and explore.                     |
| ✅ `generate_function_signatures.md` | Boosts navigability and programmatic understanding.           |
| ✅ `add_context_docs.md`             | Duplicate/alias for `generate_context_docs.md` — maybe merge. |

> 🧠 Do these once the runtime behavior is reliable. They're LLM multipliers.

---

## 🧪 Bonus: Helpers & Infra Glue

Light utility work that complements everything else — helpful but not urgent:

| Task                                 | Why                                                                   |
| ------------------------------------ | --------------------------------------------------------------------- |
| ✅ `add_default_helpers.md`          | Should be added once you see recurring logic.                         |
| ✅ `add_file_helpers_for_context.md` | Might become critical depending on path logic, but not a blocker now. |

---

## ✅ Summary: Prioritized Action Path

### 📦 Immediate

- `fix_smashlet_mtime_tracking.md`
- `explicit_output_tracking.md`
- `add_context_file_support.md`
- `context_folder_support.md`
- `inject_inputs_in_context.md`
- `tests_cli.md`

### 🛠️ Next

- `add_run_command_for_force.md`
- `status_command.md`
- `runlog_viewer_command.md`
- `centralized_logging.md` / `replace_print_with_log.md`

### 📚 After

- `generate_context_docs.md`
- `generate_file_overview.md`
- `generate_function_signatures.md`

---

## 🎯 Final Thoughts

- ✅ You don't need to cut anything from the backlog — it's focused and high-value.
- ⏳ Some stories can be **merged** (e.g., context support + context docs).
- ✅ No obvious gaps. This covers **runtime**, **CLI**, **LLM support**, and **docs**.
- 🧪 You already flagged `tests_cli.md` as high — absolutely correct. You’ll need those for confidence in mtime/output logic.
