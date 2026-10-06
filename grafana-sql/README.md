# grafana-sql

Grafana 11 on a Postgres database with the Orders seed, with the datasource and dashboard provisioned from files in `provisioning/` and `dashboards/`.

## Goal

Show Grafana reading business data straight from SQL, with nothing clicked together: the datasource and the dashboard come from files in the repo.

## Run it

Offline check (standard library only; expands `$__timeFilter` to a plain `BETWEEN` and runs each panel query on `seed.sql` in SQLite):

```
python3 verify.py
```

Expected: `ok: Paid revenue per day -> 5 rows` and `ok: Orders by status -> 3 rows`.

Live stack (Docker):

```
docker compose up -d
docker compose down -v
```

Grafana is then at http://localhost:3000 with anonymous Viewer access. The datasource password `orders` belongs to a throwaway container. Not run end to end: the stack was never started here, so provisioning in Grafana itself is untested.

## What it proves

- The panels in `dashboards/orders.json` reference the datasource uid `orders-pg` declared in `provisioning/datasources/orders.yml`.
- Both panel queries return rows on the seed data over the dashboard's 2026-01-01 to 2026-04-30 range.
- The macro expansion in `verify.py` is a stand-in for Grafana's own, so time-range edge cases are not covered.

## Trade-offs

- Grafana provisions cleanly and suits time series and operations views.
- SQL panels are hand-written, and there is little semantic modeling or ad-hoc exploration for business users.
- Provisioned dashboards are read-only copies of the files; edits in the UI are not saved back.

## When not to use it

- For business reporting with many dimensions and self-service exploration; Superset or Metabase fit better.
- For paginated PDF reports.
