# embedded-analytics

A signed-token tenant filter for an embedded dashboard query in `embed.py`, tested by `verify.py`.

## Goal

Show how a host app can embed analytics so each tenant only sees its own rows, with the tenant taken from a verified token and never from anything the browser sends.

## Run it

```
python3 verify.py
```

Expected: `ok: tenant isolation [('Ada', 200.5), ('Linus', 99.99)] [('Alan', 210.25), ('Grace', 300.0)]`

Standard library only, SQLite in memory seeded from `seed.sql`; nothing to destroy. The HMAC secret in `embed.py` is a lab-only constant. The token is a minimal `payload.signature` pair built with `hmac`, so the mechanism is visible. Real embeds use Superset guest tokens, Metabase signed embedding or Power BI embed tokens, which this code only imitates; none of those products were used.

## What it proves

- `revenue_by_customer` applies `c.tenant = ?` from the verified claim: acme gets Ada and Linus, globex gets Alan and Grace.
- A token whose signature comes from a different token is rejected with "bad signature".
- A token created with a negative lifetime is rejected as expired.

## Trade-offs

- Query-level filtering is simple and easy to test, but one missed predicate leaks data.
- Database row-level security or per-tenant schemas are a stronger second line and cost more to run.
- The lab covers neither token revocation nor key rotation.

## When not to use it

- When the BI tool already offers signed embedding with row-level filters; use that.
- When tenants need hard isolation, such as separate databases.
