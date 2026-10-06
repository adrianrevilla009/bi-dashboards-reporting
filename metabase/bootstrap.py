#!/usr/bin/env python3
"""Create cards and a dashboard in Metabase from cards.json via its API.
Usage: bootstrap.py BASE_URL SESSION_TOKEN DATABASE_ID  (add the H2 sample DB or any DB with the orders tables first)."""
import json, pathlib, sys, urllib.request

base, token, db_id = sys.argv[1], sys.argv[2], int(sys.argv[3])
spec = json.loads((pathlib.Path(__file__).parent / "cards.json").read_text())


def post(path, body):
    req = urllib.request.Request(base + path, json.dumps(body).encode(),
                                 {"Content-Type": "application/json", "X-Metabase-Session": token})
    return json.load(urllib.request.urlopen(req))


dash = post("/api/dashboard", {"name": spec["dashboard"]["name"]})
for i, c in enumerate(spec["cards"]):
    card = post("/api/card", {"name": c["name"], "display": c["display"], "visualization_settings": {},
                              "dataset_query": {"type": "native", "database": db_id, "native": {"query": c["sql"]}}})
    post(f"/api/dashboard/{dash['id']}/cards", {"cardId": card["id"], "row": i * 4, "col": 0, "size_x": 12, "size_y": 4})
print("dashboard", dash["id"])
