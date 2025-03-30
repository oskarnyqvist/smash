# 🧭 **Smash Task Analysis Protocol (for LLM or Human)**

Before starting any work, take a moment to **analyze the task itself** — not just the code.

## 🪜 Step 1: Understand and Evaluate the Task

Ask:

### ✅ 1. Does the task make sense?

- Is the goal clear and actionable?
- Is the problem real or hypothetical?
- Is there enough context to implement it?

### ✅ 2. Is the scope reasonable?

- Could this be completed in a single commit or focused session?
- Is it actually _two or more_ separate problems bundled into one?

### ✅ 3. Does the task align with project goals and architecture?

- Does it follow Smash’s values: locality, predictability, clarity?
- Is the proposed solution out of sync with how things are structured?

---

## 🪜 Step 2: Decide what to do with the task

Once you’ve evaluated the task, choose one of these paths:

| Action          | When to choose it                                          | What to do                                    |
| --------------- | ---------------------------------------------------------- | --------------------------------------------- |
| ✅ **Continue** | Task is clear, scoped, and actionable                      | Start implementation                          |
| 🛠️ **Refine**   | Task is mostly good, but needs clarification or an example | Ask for details; rewrite story                |
| ✂️ **Split**    | Task is valid but tackles multiple things                  | Break it into atomic sub-tasks                |
| ❌ **Reject**   | Task is stale, unclear, or fundamentally flawed            | Mark as obsolete or refile with a better spec |

---

## 🧠 Use these Red Flags to Trigger a Split or Rewrite

- "And also..." tasks with multiple verbs/goals
- Missing examples or expected behavior
- Vague descriptions like “add support for X” with no details
- Global refactors without clear motivation
- Tasks that imply architectural changes without context

---

# ✅ Final Checklist for Every Task

Before starting:

1. What is this changing or introducing?
2. Why does it matter — what pain is it solving?
3. What’s the best interface or design for this?
4. How will this be validated or tested?
5. Does this fit Smash’s core philosophy?
6. Could it break anything? Is it backward compatible?
7. Is the task itself usable?
   - If not, refine it, split it, or reject it.
