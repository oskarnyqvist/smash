### Comparison

Smash solves a different problem than most build or pipeline tools.

#### 🛠️ Make

- Central Makefile controls everything
- Small changes can trigger large rebuilds
- Hard to scale with many inputs and rules

**Smash:** Local files define local logic. Easy to isolate and test.

---

#### 🔁 Luigi / Airflow

- Great for scheduled jobs and DAG orchestration
- Requires boilerplate, config, and a scheduler
- Not designed for lightweight, ad-hoc builds

**Smash:** Zero infra. Just run `smash` in your repo.

---

#### 🌐 Static Site Generators

- Assume you're building a website
- Force routing, layout, and template logic
- Hard to repurpose for other kinds of content

**Smash:** No layout engine. No site assumptions. Just Python and files.
