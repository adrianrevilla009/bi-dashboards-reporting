# bi-dashboards-reporting

Seven small examples of the same Orders dataset in BI and reporting tools (Superset, Metabase, Grafana, Power BI, JasperReports, embedded analytics, a Cube semantic layer), with dashboards, metrics and tenant filters kept as reviewable files.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`superset`](./superset) | Database, dataset, chart and dashboard defined in `assets.json` and created through the Superset REST API | `python3 verify.py` (offline), `docker compose up -d` for the live stack |
| [`metabase`](./metabase) | The same data as two Metabase cards and a dashboard, defined in `cards.json` | `python3 verify.py` (offline), `docker compose up -d` for the live stack |
| [`powerbi-dax-rls`](./powerbi-dax-rls) | A Power BI semantic model sketch with DAX measures and two row-level-security roles, checked through SQL equivalents | `python3 verify.py` |
| [`grafana-sql`](./grafana-sql) | Grafana on Postgres with provisioned datasource and dashboard JSON | `python3 verify.py` (offline), `docker compose up -d` for the live stack |
| [`jasper-pdf-reports`](./jasper-pdf-reports) | A paginated PDF report from a `.jrxml` template, rendered by a small Java program | `python3 verify.py` (offline), `mvn -q compile exec:java` for the PDF |
| [`embedded-analytics`](./embedded-analytics) | Tenant isolation for an embedded dashboard query using a signed, expiring token | `python3 verify.py` |
| [`semantic-layer-cube-dbt`](./semantic-layer-cube-dbt) | Metrics and dimensions defined once in a Cube model, compiled to SQL by a small test parser | `python3 verify.py` |

All folders use the same tiny Orders domain (customers with a tenant, orders with a status and an amount).

## Prerequisites

- Python 3.10 or newer (standard library only)
- Docker with Compose, only for the live Superset, Metabase and Grafana stacks
- Java 21 and Maven, only for the real PDF render in `jasper-pdf-reports`

## How to read it

Start with `superset`, then `metabase` to compare the same data in two tools. The Power BI, Grafana, Jasper, embedding and semantic-layer folders are independent. Every folder has an offline `verify.py`. The Superset, Metabase, Grafana and Jasper live runs were not executed end to end; each folder README says so.
