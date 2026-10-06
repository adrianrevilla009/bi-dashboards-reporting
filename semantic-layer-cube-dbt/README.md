# semantic-layer-cube-dbt

A Cube data model in `model/orders.yml` for the Orders domain, with a small Python check that compiles a metric query from it.

## Goal

Define business metrics (`count`, `paid_revenue`) and dimensions (`tenant`, `status`, `ordered_month`) once, so every dashboard asks the semantic layer instead of rewriting SQL.

## Run it

```
python3 verify.py
```

Expected: `ok: semantic layer compiled [('acme', 300.49), ('globex', 510.25)]`

Standard library only. `verify.py` has a tiny regex parser for this one YAML file; it is not Cube's own compiler. Not run end to end: Cube itself was never started here, and no dbt project exists in this folder. To try the real thing, run a `cubejs/cube` container against a Postgres loaded with `seed.sql` and mount `model/` as its model folder. Cube was chosen over dbt's metrics layer because it serves queries to BI tools over an API.

## What it proves

- `paid_revenue` carries the `status = 'PAID'` filter in one place in `orders.yml`.
- The SQL compiled from the model for `paid_revenue` by `tenant` equals a hand-written query: acme 300.49, globex 510.25.
- The `count` measure by tenant gives 4 orders each. The `ordered_month` and `status` dimensions are defined but not exercised by the check.

## Trade-offs

- A semantic layer gives consistent definitions, caching and access control across tools.
- It adds a service to run, a modeling language to learn and a second place to look when numbers are wrong.
- The regex parser only handles the shape of this file and would break on richer models.

## When not to use it

- With one dashboard tool and a handful of metrics, where a SQL view does the same job.
