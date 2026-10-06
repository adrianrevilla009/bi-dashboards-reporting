# jasper-pdf-reports

A JasperReports template (`orders.jrxml`) and a Java 21 program (`RenderReport.java`) that fills it from an in-memory SQLite database and writes a PDF.

## Goal

Produce a paginated PDF of the Orders data from a report template that lives in the repo as code.

## Run it

Offline check (standard library only; parses the jrxml, compares its fields with the query columns and runs the query on `seed.sql` in SQLite):

```
python3 verify.py
```

Expected: `ok: jrxml fields ['customer', 'status', 'amount'] rows 8`

Real render (Maven and network access for dependencies):

```
mvn -q compile exec:java
```

This should write `target/orders.pdf` and print the page count. Not run end to end: the Maven build and the PDF were never produced here, so the layout is unseen. No server or credentials are involved. Versions are pinned in `pom.xml` (JasperReports 6.21.3, sqlite-jdbc 3.46.1.0).

## What it proves

- The jrxml field list (`customer`, `status`, `amount`) matches the columns of its own query.
- The query returns all 8 seed orders, with amounts adding up to 930.74.
- The report definition is one reviewable XML file, so the query and layout change together.

## Trade-offs

- Jasper gives paginated, printable output with no BI server.
- The XML is verbose and layout is fiddly without Jaspersoft Studio.
- The report has no interactivity.
- The check covers the data contract only, not how the PDF looks.

## When not to use it

- For interactive dashboards or data exploration.
- When a simple HTML-to-PDF template would do.
