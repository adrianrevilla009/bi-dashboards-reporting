#!/usr/bin/env python3
"""Offline check: every card's SQL in cards.json returns its expected rows on the seed data."""
import json, pathlib, sqlite3

here = pathlib.Path(__file__).parent
spec = json.loads((here / "cards.json").read_text())
db = sqlite3.connect(":memory:")
db.executescript((here / "seed.sql").read_text())
for c in spec["cards"]:
    got = [list(r) for r in db.execute(c["sql"])]
    assert got == c["expected"], (c["name"], got)
    print("ok:", c["name"])
