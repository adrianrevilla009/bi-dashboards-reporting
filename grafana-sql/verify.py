#!/usr/bin/env python3
"""Offline check: dashboard JSON is well formed, uses the provisioned datasource uid, and every panel query
runs on the seed data once Grafana macros are expanded to plain SQL."""
import json, pathlib, re, sqlite3

here = pathlib.Path(__file__).parent
dash = json.loads((here / "dashboards/orders.json").read_text())
provisioned = (here / "provisioning/datasources/orders.yml").read_text()
uid = re.search(r"uid:\s*(\S+)", provisioned).group(1)
db = sqlite3.connect(":memory:")
db.executescript((here / "seed.sql").read_text())
start, end = dash["time"]["from"][:10], dash["time"]["to"][:10]
for p in dash["panels"]:
    assert p["datasource"]["uid"] == uid, f"panel {p['id']} uses unknown datasource"
    sql = re.sub(r"\$__timeFilter\((\w+)\)", rf"\1 BETWEEN '{start}' AND '{end}'", p["targets"][0]["rawSql"])
    rows = db.execute(sql).fetchall()
    assert rows, f"panel {p['id']} returned no rows"
    print(f"ok: {p['title']} -> {len(rows)} rows")
