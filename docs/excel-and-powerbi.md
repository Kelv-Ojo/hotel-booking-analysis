# Excel and Power BI implementation notes

## Verified Excel workbook

`excel/Hotel Reporting.xlsx` contains a formula-driven Report, a native MonthlySource Excel table, and Definitions. The source covers all 119,390 bookings aggregated into 176 rows; it is not a sample. Choose an arrival year and hotel in the amber cells. SUMIFS recomputes counts and weighted cancellation rates; the chart references those monthly results. Channel reconciliation differences should be zero.

All six year/hotel combinations were checked against the Python aggregates. The package was inspected for formulas, cached results, charts, validations and table definitions. Native Excel refresh has not been tested in Excel itself.

### Power Query companion

The workbook does not contain an embedded Power Query connection. To use the supplied M code, create a text parameter named CsvPath pointing to the repository's `reports/excel_source.csv`, then create a blank query, paste `ImportMonthly.pq` into Advanced Editor, and load it as a separate MonthlyImport table. Validate that the imported bookings sum to 119,390 before replacing any source data. The M code is supplied for review; execution in Excel remains unverified.

### PivotTable exercise

Native PivotTables are not embedded because the available spreadsheet exporter does not reliably preserve them. In Excel, insert a PivotTable from MonthlySource: rows Hotel, columns Year, values SUM of Bookings and SUM of Canceled flag. Add Channel as a filter. Calculate cancellation rates from summed counts outside the pivot; do not average precomputed rates. Grand totals should be 119,390 bookings and 44,224 canceled flags.

## Original Power BI report

The PBIX, PDF and screenshot are preserved from the existing project. They are earlier work, not a newly refreshed dashboard. The PDF's 36,483 YTD card has a different scope from the full dataset, and its date range starts before the first arrival date. Do not use that card as the full-snapshot total.

### Rebuild specification

1. Run `python src/analyze.py`. For Power BI import, use the normalized CSV files created in reports/model/.
2. Import bookings, hotels, channels, segments and dates. Set arrival_date/date_id to Date and dimension IDs to Whole Number.
3. Create single-direction one-to-many relationships from dimensions into bookings, with dates.date_id linked to bookings.arrival_date. Verify each dimension key is unique.
4. Add the companion measures in `powerbi/measures.dax` one at a time; format Cancellation Rate as a percentage.
5. Use arrival year and hotel slicers. Show bookings, canceled flag, checked out and no-show cards; a monthly booking trend; and channel cancellation counts and rates with denominators.
6. Label 2015 and 2017 as partial years. Avoid YTD labels without a clearly selected cutoff and comparison period. Explain that canceled flags include no-shows.
7. With all filters cleared, verify 119,390 bookings, 44,224 canceled flags, 75,166 check-outs and 1,207 no-shows. Check both hotels against reports/metrics.json.

Power BI Desktop is not available in this session, so these rebuild steps and DAX measures have not been executed. No PBIX repair, service publication or live dashboard link is claimed.
