### Why Smash?

Traditional tools make local content workflows harder than they should be.

- **Make** is powerful but brittle. One global file controls everything.
- **Luigi / Airflow** are great for orchestration, but overkill for local pipelines.
- **Static site generators** assume you're building a website.

Smash is different:

- No global config
- No DAGs
- No templating assumptions

Just plain Python files, colocated with the content they transform.
