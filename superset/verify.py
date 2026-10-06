#!/usr/bin/env python3
"""Offline check: the dataset SQL in assets.json runs on the seed data and gives the expected totals."""
import json, sqlite3, pathlib

here = pathlib.Path(__file__).parent
assets = json.loads((here / "assets.json").read_text())
db = sqlite3.connect(":memory:")
db.executescript((here / "seed.sql").read_text())
rows = dict(db.execute(assets["dataset"]["sql"]).fetchall())
assert rows == {"2026-01": 200.5, "2026-02": 300.0, "2026-03": 310.24}, rows
assert assets["chart"]["params"]["metrics"] == ["revenue"] and assets["chart"]["params"]["x_axis"] == "month"
print("ok: dataset SQL returns", rows)
