#!/usr/bin/env python3
"""Create database, dataset, chart and dashboard in Superset from assets.json via its REST API."""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8088"
assets = json.load(open(__file__.rsplit("/", 1)[0] + "/assets.json"))


def call(path, body=None, token=None, method=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None,
                                 method=method, headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    return json.load(urllib.request.urlopen(req))


token = call("/api/v1/security/login", {"username": "admin", "password": "admin", "provider": "db", "refresh": True})["access_token"]
db_id = call("/api/v1/database/", assets["database"], token)["id"]
ds_id = call("/api/v1/dataset/", {"database": db_id, "schema": "public", "sql": assets["dataset"]["sql"],
                                  "table_name": assets["dataset"]["table_name"]}, token)["id"]
chart = dict(assets["chart"], datasource_id=ds_id, datasource_type="table", params=json.dumps(assets["chart"]["params"]))
chart_id = call("/api/v1/chart/", chart, token)["id"]
dash_id = call("/api/v1/dashboard/", assets["dashboard"], token)["id"]
call(f"/api/v1/chart/{chart_id}", {"dashboards": [dash_id]}, token, "PUT")
print("dashboard", dash_id, "chart", chart_id)
