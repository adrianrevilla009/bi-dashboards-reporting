#!/usr/bin/env python3
"""Offline check: orders.jrxml is well-formed XML, its fields match the query columns, and the query runs on the seed data."""
import pathlib, sqlite3, xml.etree.ElementTree as ET

here = pathlib.Path(__file__).parent
ns = {"j": "http://jasperreports.sourceforge.net/jasperreports"}
root = ET.parse(here / "orders.jrxml").getroot()
sql = root.find("j:queryString", ns).text.strip()
fields = [f.get("name") for f in root.findall("j:field", ns)]
db = sqlite3.connect(":memory:")
db.executescript((here / "seed.sql").read_text())
cur = db.execute(sql)
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
assert cols == fields, (cols, fields)
assert len(rows) == 8 and round(sum(r[2] for r in rows), 2) == 930.74, rows
print("ok: jrxml fields", fields, "rows", len(rows))
