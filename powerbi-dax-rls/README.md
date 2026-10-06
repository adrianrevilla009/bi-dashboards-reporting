# powerbi-dax-rls

A readable sketch of a Power BI semantic model in `model.json`: two tables, a relationship, two DAX measures and two row-level-security roles.

## Goal

Show how DAX measures and per-tenant row-level security for Orders are described, and check the numbers they must produce without Power BI.

## Run it

```
python3 verify.py
```

Expected: three lines, `ok: none {'Paid Revenue': 810.74, 'Cancel Rate': 0.25}`, then `ok: TenantAcme ...` with 300.49 and `ok: TenantGlobex ...` with 510.25.

Not run end to end: Power BI Desktop is Windows-only and was not available. `model.json` is a TMSL-style sketch, not a file Desktop can open. To use it, recreate the measures and roles in Desktop (Modeling, Manage roles). The DAX text is never executed here. Nothing is deployed, so there is nothing to destroy and no cost.

## What it proves

- Every `Table[column]` reference in the measures, roles and relationship exists in the table list of `model.json`.
- Each measure (`Paid Revenue`, `Cancel Rate`) has a `sqlEquivalent` that gives 810.74 and 0.25 on the seed data with no role applied.
- With a role's predicate added, paid revenue drops to the tenant's rows: 300.49 for `TenantAcme` and 510.25 for `TenantGlobex`.

## Trade-offs

- The SQL parity check catches wrong filters and column typos cheaply, but not DAX semantics such as filter context or bidirectional relationships.
- The SQL equivalents and the DAX are written by hand, so they can drift apart.
- Real validation needs Desktop or an XMLA endpoint, which means paid capacity.

## When not to use it

- When you have Power BI Desktop or Fabric available; test the real model with DAX Studio or Tabular Editor.
- When tenant isolation must be enforced in the database for every consumer, not only in one tool.
