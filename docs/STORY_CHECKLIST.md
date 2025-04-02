# 🧭 Smash Task Analysis Protocol (for LLM or Human)

## Step 1: Think Before You Build

Before you touch code, **analyze the task**:

- ❓ What are we changing or introducing?
- 💥 Why does it matter? What's the pain?
- 🎯 What's the right interface or behavior?
- 🧪 How will we test it?
- 🧱 Does this align with Smash's values (local-first, clear, Pythonic)?
- 🔁 Is it backwards-compatible? Can it break anything?

Use this to **clarify intent and scope**, not to write a long document.

---

## Step 2: Write a Dense, Focused Story

After you've thought it through, write the task as a **clear, single-purpose unit of work**.

### ✅ A good task story should:

- Fit in one focused commit or PR
- Be specific about behavior, inputs/outputs, and rules
- Avoid vague verbs like “support”, “handle”, “improve”
- Skip fluff — just say what should exist and how it should work

---

### ✅ Example (Concise Style)

> TASK: Add detailed per-smashlet runlog metadata
>
> Extend `.smash/runlog.json` to store:
>
> - `last_run`: timestamp
> - `last_skip`: timestamp
> - `runs`: count
>
> Treat float values as `last_run` for legacy support.  
> On run: set `last_run`, increment `runs`.  
> On skip: update `last_skip`.
>
> Add tests for structured vs legacy formats, skip vs run behavior.

---

## Step 3: Split, Refine, or Reject if Needed

Use this table when evaluating task proposals:

| Action          | When to choose it                               |
| --------------- | ----------------------------------------------- |
| ✅ **Continue** | Task is clear, scoped, and actionable           |
| 🛠️ **Refine**   | Task needs clarification or concrete behavior   |
| ✂️ **Split**    | Task tackles multiple things at once            |
| ❌ **Reject**   | Task is stale, vague, or not aligned with goals |

---

## Red Flags to Watch For

- "And also..." tasks with multiple goals
- Vague requests ("add support for X")
- Global refactors without motivation
- Tasks that imply major changes without context

---

✅ **Think deeply. Write tightly. Build clearly.**
