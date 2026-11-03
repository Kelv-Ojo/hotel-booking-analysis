# Screenshot and visual provenance

Captured or rebuilt locally on 30 October 2026. No mock dashboards or generated application screenshots.

- `excel-report.png` — Actual Excel reporting output with City Hotel and 2016 selected. The filtered preview is a different scope from the complete 119,390-row snapshot. Source: `excel/report-preview.png`.
- `sql-results.png` — Rendered output from the actual SQLite segment query: joins, grouped cancellation counts and DENSE_RANK. First eight rows shown; flags include no-shows. This is a query-output capture, not a database-IDE screenshot. Source: `sql/segments.sql` against `reports/hotel.db`, rendered by `src/render_sql_preview.py` to `assets/screenshots/sql-results.html` and captured in the browser.

- `powerbi-original.png` — preserved earlier Power BI report. Original YTD/date/status definition issues remain; this image is historical evidence, not the verified full-source result. Source: `powerbi/original-dashboard.png`.

To refresh the SQL page, run the documented analysis first, then `python src/render_sql_preview.py`. Open the generated HTML in a browser and capture the report.
