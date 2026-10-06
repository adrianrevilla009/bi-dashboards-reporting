#!/usr/bin/env python3
"""Offline check: each tenant token only sees its own rows; tampered and expired tokens are rejected."""
import pathlib, sqlite3, time
from embed import revenue_by_customer, sign_token, verify_token

db = sqlite3.connect(":memory:")
db.executescript((pathlib.Path(__file__).parent / "seed.sql").read_text())

acme = revenue_by_customer(db, sign_token("acme"))
globex = revenue_by_customer(db, sign_token("globex"))
assert acme == [("Ada", 200.5), ("Linus", 99.99)], acme
assert globex == [("Alan", 210.25), ("Grace", 300.0)], globex

forged = sign_token("acme").split(".")[0] + "." + sign_token("globex").split(".")[1]
for bad in (forged, sign_token("acme", ttl=-10)):
    try:
        verify_token(bad)
        raise SystemExit("token should have been rejected")
    except PermissionError:
        pass
print("ok: tenant isolation", acme, globex)
