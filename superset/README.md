# superset

An Orders dashboard for Apache Superset defined in `assets.json` and created by `bootstrap.py` through the REST API.

## Goal

Define a Superset database, virtual dataset, chart and dashboard as plain data, so the dashboard can be reviewed in a diff and re-applied to a fresh instance.

## Run it

Offline check (standard library only; runs the dataset SQL from `assets.json` against `seed.sql` in SQLite):

```
python3 verify.py
```

Expected: `ok: dataset SQL returns {'2026-01': 200.5, '2026-02': 300, '2026-03': 310.24}`

Live stack (Docker; first start takes a few minutes):

```
docker compose up -d
python3 bootstrap.py http://localhost:8088
docker compose down -v
```

Login is `admin` / `admin`, a throwaway value for this local container. `docker compose down -v` removes the containers and data. Not run end to end: the compose stack and `bootstrap.py` were never started here, so the REST calls follow the Superset 4.1 API but are untested.

## What it proves

- The dataset SQL in `assets.json` returns paid revenue of 200.5, 300 and 310.24 for January to March 2026 on the seed data.
- The chart definition points at the `month` and `revenue` columns that the dataset SQL produces.
- The live database is Postgres seeded from `seed.pg.sql` (same rows as `seed.sql`); the offline check uses SQLite for speed.

## Trade-offs

- The REST bootstrap is short and diffable but not idempotent: running it twice creates duplicates.
- Superset's own export/import bundle is idempotent but harder to read in review.
- The compose command installs `psycopg2-binary` on every start, which needs network access.

## When not to use it

- When you need many dashboards managed at scale; use export/import bundles or Terraform instead.
- When a lighter tool such as Metabase or Grafana already covers the need.
