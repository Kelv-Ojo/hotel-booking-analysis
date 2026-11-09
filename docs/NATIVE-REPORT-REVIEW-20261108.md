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

## Final visual acceptance, completed 9 November 2026

The requested interaction acceptance is complete for the documented cases. See [native observation record](../reports/native_visual_acceptance.json). This covers every slicer type and every data-visual family; it is not a claim to test every possible value combination or future Power BI release.

| Native action | Verified result |
|---|---|
| Arrival date 1–31 July 2015 | 2,776 bookings, 1,517 checkouts, 1,259 cancellation flags |
| Month-Year Jul 2015, full date range | Same totals, confirming the common arrival-date basis |
| Country PRT and year 2016 | 22,321 bookings, 12,405 flags; channel and monthly charts respond |
| Add market segment Direct | 2,652 bookings, 513 flags; country, channel and monthly charts respond |
| Clear country, retain Direct and 2016 | 5,663 bookings, 867 flags, 84.7% checkout rate |
| July lower matrices | Every nonempty adult/weekend-night cell matches independent workbook counts; totals 1,517 / 1,259 |
| July rate and deposit charts | Adult/customer cancellation percentages and 1,517 / 1,029 No Deposit statuses match source; selecting and clearing the deposit bar updates/restores other visuals |
| Revised chart-driven filtering | Direct segment chart gives 5,663 / 4,796 / 867; selecting No Deposit gives 36,173 checkouts / 13,609 flags in 2016 |

Original native cross-highlighting left background totals visible beside recalculated rate labels. The final page explicitly uses DataFilter for 154 links from eleven selectable visuals to the other data visuals. This makes each selected category's denominator clear. Static checks verify every source/target exists, links are unique and all intended pairs use DataFilter; native representative chart selections confirm the behaviour. Selecting another chart replaces the previous chart selection; use slicers for retained combinations. Self-selection retains the native highlight indication.

The report now labels Arrival date, both adult/weekend-night matrices, partial arrival years, inclusion of no-shows, historical associations and small-group caution. Caveats render in dark text with readable contrast. Default year/hotel/month selections are cleared. The original 24 visual containers are preserved, with one added caveat label; original visual fields and measures remain intact.

Screenshots: [date range](../assets/screenshots/hotel-test-date-july2015.png), [Month-Year](../assets/screenshots/hotel-test-month-july2015.png), [country](../assets/screenshots/hotel-test-country-prt2016.png), [combined slicers](../assets/screenshots/hotel-test-country-segment2016.png), [matrix cells](../assets/screenshots/hotel-test-deposit-matrices-july.png), [final filtering](../assets/screenshots/hotel-test-final-donut-filter.png), [matrix labels](../assets/screenshots/hotel-test-final-matrix-labels.png), [report caveats](../assets/screenshots/hotel-final-caveats.png).

Recheck the recorded workbook comparisons with `python src/check_native_observations.py PATH_TO_WORKBOOK` and openpyxl installed. This reads the source and compares transcribed native observations; it does not automate Power BI or falsely certify runtime interactions.

Desktop Excel remains unavailable. The formula workbook is preserved, but embedded native Power Query connections, PivotTables and Excel refresh remain unverified and unfinished.

## Final export and reopen

On 9 November 2026 the final project was saved, exported to the separate reviewed PBIX, closed and reopened in Power BI Desktop. Arrival-date label, readable caveats and default cleared filters persisted; full cards showed 119,390 bookings, 75,166 checkouts and 44,224 flags with no missing-data warning. Selecting Direct in the reopened market-segment chart produced 12,606 bookings, 10,672 checkouts and 1,934 flags; clearing it restored the full snapshot. [Reopen interaction evidence](../assets/screenshots/hotel-final-reopen-interaction.png).

Final reviewed PBIX SHA256: `e472b23be365317c9856bb6a64d1cb04e2513a6b6067809343411b26cfa6027a`. The original remains unchanged. No Power BI service upload or public interactive hosting is claimed.
