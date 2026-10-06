#!/usr/bin/env python3
"""Offline check of the semantic model: structure, DAX/SQL parity for measures, and row-level security.
DAX itself is not executed; each measure carries a SQL equivalent that runs on the seed data with the role's predicate."""
import json, pathlib, re, sqlite3

here = pathlib.Path(__file__).parent
model = json.loads((here / "model.json").read_text())
db = sqlite3.connect(":memory:")
db.executescript((here / "seed.sql").read_text())

tables = {t["name"]: set(t["columns"]) for t in model["tables"]}
for ref in re.findall(r"(\w+)\[(\w+)\]", json.dumps(model["measures"] + model["roles"] + model["relationships"])):
    assert ref[1] in tables.get(ref[0], ()), f"unknown column {ref}"


def run(measure, predicate=None):
    sql = measure["sqlEquivalent"]
    if predicate:
        sql += (" AND " if " WHERE " in sql else " WHERE ") + predicate
    return round(db.execute(sql).fetchone()[0], 2)


for scope, want in model["expected"].items():
    preds = [p["sqlPredicate"] for r in model["roles"] if r["name"] == scope for p in r["tablePermissions"]]
    for m in model["measures"]:
        got = run(m, preds[0] if preds else None)
        assert got == want[m["name"]], (scope, m["name"], got, want[m["name"]])
    print("ok:", scope, want)
