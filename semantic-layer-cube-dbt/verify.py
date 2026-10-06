#!/usr/bin/env python3
"""Offline check: compile a metric query (measure x dimension) from the Cube model into SQL, run it on the seed
data, and compare with a hand-written query. Shows that the semantic layer is one definition reused by every query."""
import pathlib, re, sqlite3

here = pathlib.Path(__file__).parent
model = (here / "model/orders.yml").read_text()
db = sqlite3.connect(":memory:")
db.executescript((here / "seed.sql").read_text())


def block(kind, name):
    """Return the YAML list item `- name: <name>` under `kind:` as text (tiny parser for this file's shape)."""
    section = re.search(rf"^    {kind}:\n(.*?)(?=^    \w+:|^  - name|\Z)", model, re.M | re.S).group(1)
    return re.search(rf"      - name: {name}\n(.*?)(?=^      - name|\Z)", section, re.M | re.S).group(0)


def measure_sql(name):
    b = block("measures", name)
    col = re.search(r"sql: (\w+)", b)
    cond = re.search(r"filters:\n\s+- sql: \"(.*)\"", b)
    agg = {"sum": "SUM", "count": "COUNT"}[re.search(r"type: (\w+)", b).group(1)]
    expr = f"{agg}({col.group(1) if col else '*'})"
    if cond:
        expr = f"{agg}(CASE WHEN {cond.group(1).replace('{CUBE}', 'orders')} THEN {col.group(1)} END)"
    return expr


def compile_query(measure, dimension):
    return (f"SELECT customers.{dimension}, {measure_sql(measure)} FROM orders "
            f"JOIN customers ON orders.customer_id = customers.id GROUP BY 1 ORDER BY 1")


got = db.execute(compile_query("paid_revenue", "tenant")).fetchall()
want = db.execute(
    "SELECT c.tenant, SUM(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id "
    "WHERE o.status = 'PAID' GROUP BY c.tenant ORDER BY c.tenant").fetchall()
assert got == want == [("acme", 300.49), ("globex", 510.25)], (got, want)
assert db.execute(compile_query("count", "tenant")).fetchall() == [("acme", 4), ("globex", 4)]
print("ok: semantic layer compiled", got)
