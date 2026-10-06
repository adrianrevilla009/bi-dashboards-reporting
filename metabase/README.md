# metabase

Two Metabase cards and a dashboard defined in `cards.json` and created by `bootstrap.py` through the Metabase API.

## Goal

Build the same Orders dataset as in the `superset` folder in Metabase, with each card holding its SQL and the rows it must return.

## Run it

Offline check (standard library only; runs every card's SQL on `seed.sql` in SQLite and compares with the `expected` rows):

```
python3 verify.py
```

Expected: `ok: Paid revenue by month` and `ok: Orders by status`.

Live stack (Docker):

```
docker compose up -d
# finish the setup wizard at http://localhost:3000 and add a database holding the orders tables, then:
python3 bootstrap.py http://localhost:3000 <session-token> <database-id>
docker compose down -v
```

Not run end to end: Metabase was never started here, so the API calls in `bootstrap.py` (written for v0.50) are untested. The setup wizard stays manual so that no credentials are stored in the repo. `docker-compose.yml` mounts `seed.sql` only for reference; load it into your chosen database yourself.

## What it proves

- "Paid revenue by month" returns 200.5, 300 and 310.24 for January to March 2026.
- "Orders by status" returns CANCELLED 2, NEW 1, PAID 5.
- These are the same numbers as the `superset` dataset, so both tools agree on the data.

## Trade-offs

- Metabase is quick for non-technical users to explore, but dashboards as code is weaker: the API is scriptable and native serialization is an Enterprise feature.
- `bootstrap.py` is not idempotent; each run creates a new dashboard and new cards.
- The first-run setup is manual.

## When not to use it

- When metrics must be governed once and shared across tools; use a semantic layer such as `semantic-layer-cube-dbt`.
- When you need pixel-exact paginated reports or fully versioned dashboards on the open-source edition.
