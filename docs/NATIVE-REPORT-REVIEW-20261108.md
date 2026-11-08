# Native hotel report review, 8 November 2026

## Delivered review copy

The original `powerbi/Hotel Bookings.pbix` is unchanged (SHA256 `564b25bd09cdaadaefc8e163bc3f6f5474c048f43edb5d2a39a28ebe5c244332`). The separate `Hotel Bookings-reviewed-20261108.pbix` was saved from Power BI Desktop after native refresh. Its editable PBIP/TMDL definitions are included; local caches and machine settings are excluded.

The previous Save As blocker is resolved. The original source workbook was recovered privately from the original hotel archive. Its SHA256 is `8cba074e328df64b50d480ebef415bfa89dd93a55b2020f41fc7d336b84dcb28`, matching the pre-existing provenance record. Every shared source field in all 119,390 rows matches the repository CSV. The private assignment archive/report is not redistributed.

## Repairs

- Calendar now filters calculated ArrivalDate, rather than reservation_status_date. Arrival dates run 2015-07-01 through 2017-08-31.
- Report visual bindings use selected-period counts instead of misleading TOTALYTD results. Checked Out explicitly filters Check-Out status; Cancellation Flags includes no-shows.
- Stale workbook paths are replaced by SourceWorkbookPath. Four text NA values in children are converted to null before numeric conversion, preserving all bookings. Native refresh completed without the previous conversion warning.
- Country labels retain the original lookup names and use the original code plus `(code)` for unmapped codes. Missing codes are labelled Not recorded, rather than conflated with unmapped countries.
- Original visual positions and styling are retained. Legacy measures remain in the model for comparison; reviewed visual bindings use explicit measures.

## Executed native checks

Six hotel/arrival-year DAX groups match independent workbook counts exactly: [reconciliation JSON](../reports/native_hotel_reconciliation.json), [DAX screenshot](../assets/screenshots/hotel-native-six-scope-check.png).

Native Power Query refreshed MonthlyImport using the companion Excel M script: 176 rows, 119,390 bookings, 44,224 cancellation flags, 75,166 checkouts, 1,207 no-shows. Source table has 119,390 rows and four missing children values. [Native output](../assets/screenshots/hotel-native-refresh-check.png). This tests M in Power BI, not Excel PivotTables or Excel refresh.

Native dimension query found 178 country keys and 178 distinct keys, no blank labels, 488 missing-country bookings, 793 calendar rows and distinct dates, and no orphan arrival dates. DAX COUNTROWS on an empty set displays BLANK. [Native output](../assets/screenshots/hotel-native-dimensions.png).

Year slicer 2016 gave 56,707 / 36,370 / 20,337 bookings/checkouts/cancellation flags. Adding City Hotel gave 38,140 / 22,733 / 15,407, matching source data. [Interaction screenshot](../assets/screenshots/hotel-native-city-2016.png). Clearing selections restored 119,390 / 75,166 / 44,224. Channel full totals observed: TA/TO 97,870; Direct 14,645; Corporate 6,677; GDS 193; Undefined 5.

## Refresh setup

For a matching full source workbook, set the SourceWorkbookPath text parameter in Power Query. The review machine uses the generic path `C:\PortfolioData\hotel-booking-analysis\Hotel Bookings-source.xlsx`. Set CsvPath to this repository's `reports/excel_source.csv` for MonthlyImport. Full workbook has the hotel_bookings and Summary sheets. Use `python src/reconcile_original_workbook.py PATH_TO_WORKBOOK` with openpyxl installed to confirm the source. Do not substitute another snapshot silently.

## Still required before Done

The model, refresh and representative year/hotel interactions are verified, not every possible visual interaction. Finish a recorded acceptance matrix for date-range boundaries, Month-Year, country and market-segment slicers; chart cross-filter/highlight behaviour; every monthly plotted point and every country/segment subtotal including missing codes. Label the date slicer explicitly as arrival date and add partial-year/no-show notes directly in the report. The exported PBIX was reopened successfully: the saved 2016 selection retained 56,707 bookings and 36,370 checkouts with no missing-data warning. Until then the board card remains In Progress.

Desktop Excel is unavailable. The formula workbook is preserved, but embedded native Power Query connections, PivotTables and Excel refresh remain unverified and unfinished.
