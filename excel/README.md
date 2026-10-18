# Workbook contents and regeneration

Hotel Reporting.xlsx is a saved formula-driven report generated with the OpenAI artifact-tool spreadsheet runtime. It can be opened without that runtime; no macros or external connections are included.

The workbook contains:

- Report: year/hotel selectors, monthly results, channel results, reconciliation differences and a source-linked chart.
- Monthly source: all 119,390 bookings represented in 176 month/hotel/channel aggregates, stored as a native Excel table.
- Definitions: source, metric definitions and implementation limitations.

The builder is in `build_report.mjs`. It requires Node.js and the `@oai/artifact-tool` package available in the Codex workspace dependency runtime. It is not an ordinary pip dependency. To regenerate in that environment, run the Python analysis first, then run the builder from its own directory with that package on Node's module resolution path. The builder reads `source.json` produced by the Python pipeline and saves the workbook and previews in this folder. The prebuilt workbook is included for readers without the authoring runtime.

`validation.json` records the six source comparisons. `ImportMonthly.pq` is a separate Power Query script, not an embedded or tested query. See the implementation notes for Power Query and native PivotTable setup. Native Excel recalculation and refresh have not been verified in the Excel application.
