# Native Excel completion route

Updated 9 November 2026. Desktop Excel is unavailable and there is no connected Excel document session. Kelvin confirmed he has neither desktop Excel nor a Microsoft 365 Business/Enterprise account. No purchase, subscription, installation or native Excel result is claimed.

## Available options

1. Use an existing licensed desktop Excel installation on a machine Kelvin is authorised to use. This is the most direct route for the board's desktop refresh requirement. Work on a copy named Hotel Reporting-native.xlsx, preserving the original workbook.
2. If a suitable Microsoft 365 account becomes available, Excel for the web is a legitimate native alternative for supported sources: Microsoft documents query viewing/refresh for subscribers and additional import/edit features for Business or Enterprise plans. Account-specific capability and native execution still need checking. This would establish **web** functionality; it would not certify desktop Excel. No paid account is currently available for this task.
3. LibreOffice, Google Sheets, Python and the existing Power BI M-engine test do not establish Excel Power Query/PivotTable behaviour. Retain the usable formula workbook until native checks are possible.

[Microsoft: Power Query in Excel for the web](https://support.microsoft.com/en-us/excel/use-power-query-in-excel-for-the-web), [supported data sources](https://support.microsoft.com/en-us/excel/power-query-data-sources-in-excel-versions).

## Desktop implementation, without replacing the original report

1. Open a copy of Hotel Reporting.xlsx. Keep Report, Monthly source and Definitions. Record the Excel version and build.
2. Data → Get Data → Launch Power Query Editor. Create a text parameter CsvPath with the local reports/excel_source.csv path. Create a blank query named MonthlyImport and paste ImportMonthly.pq. Load it to a **new** worksheet/table, leaving MonthlySource untouched until comparison passes.
3. Confirm the eight CSV fields and count types, 176 aggregate rows, unique year/month/hotel/channel keys and no query errors. Verify bookings = canceled + checked_out and no_shows ≤ canceled. Canceled includes no-shows; do not add no-shows a second time.
4. Insert a native PivotTable from the imported table. Rows: hotel; columns: year; filter: distribution_channel; values: **Sum** of bookings, canceled, checked_out and no_shows. Do not use Count or average cancellation percentages. Use summed canceled / summed bookings outside the pivot for the weighted rate.
5. Compare all six year/hotel scopes against validation.json, not just grand totals. Full totals: 119,390 bookings, 44,224 cancellation flags, 75,166 checked-out records and 1,207 no-shows. Check the existing formula Report at the same selectors; E34/E35 should remain zero.
6. Refresh the query to completion, then refresh the PivotTable. Check Refresh All, query connection and refresh-on-open/background settings explicitly; do not assume the pivot waited for an asynchronous query.
7. In a **disposable source/workbook copy**, change one aggregate row by +1 booking and +1 checked_out. Point CsvPath at that copy, refresh query and pivot, and verify exactly those totals change. The original dataset remains untouched. Restore CsvPath, refresh again and verify the original totals. This demonstrates refresh rather than a cached result.
8. Save, close and reopen the native workbook. Confirm query/connection and PivotTable persist, refresh succeeds and the original six scopes still reconcile. Capture screenshots showing application, selected filters and results. Keep credentials/local paths out of published screenshots.

For web use, File.Contents(CsvPath) cannot be assumed to access a Windows local path. Select a documented supported cloud source and verify the connection in the actual account; no existing local M script has been certified in Excel web.

## Evidence needed before Done

Keep the saved native workbook, Excel version/build, query/PivotTable settings, six scope results, disposable-copy refresh and restore evidence, and reopen screenshots. Until these exist, the Excel task remains Ready. The companion M script has already been executed in Power BI; do not rerun that completed check as a substitute.
