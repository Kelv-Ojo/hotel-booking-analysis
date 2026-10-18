# Hotel booking findings

The full source snapshot contains **119,390 bookings**, arriving from **2015-07-01 to 2017-08-31**. **44,224 (37.0%)** have the source cancellation flag. This flag includes no-shows; 1,207 are labelled No-Show and 75,166 Check-Out.

## Findings and recommended investigation

- City Hotel cancellation flag rate: **41.7%**; Resort Hotel: **27.8%**. Investigate channel and lead-time mix before attributing the difference to hotel operations.
- Examine high-volume segments in `segments.csv` for targeted confirmation or communication trials. Rate rankings exclude groups below 100 bookings but do not adjust for confounding.
- Compare matching months across years. The dataset starts in July 2015 and ends in August 2017, so whole-year totals are not directly comparable. Month-to-month changes are descriptive and seasonal.

## Reporting corrections and limits

The original Power BI PDF shows 36,483 in its YTD card, a different scope from the full 119,390-row source; these must not be described as the same population. Its date axis includes 2014, while source arrival dates begin in July 2015. The original PBIX and PDF are preserved as earlier work; they have not been repaired or reopened in Power BI Desktop here. Use the verified SQL outputs and Excel report for full-snapshot metrics.

Do not call all non-canceled bookings completed stays. Use the explicit reservation_status='Check-Out' count for checked-out bookings, and label the cancellation flag as including no-shows. A booking is not necessarily a distinct guest. Repeated identical business fields can represent distinct bookings; no deduplication was performed without a source booking ID. Added booking IDs are original workbook row numbers, not business-issued IDs.

No room inventory, costs, payment transactions or treatment data is supplied. Occupancy, profit, realized revenue and causal effects cannot be established. No current hotel performance or savings is claimed. All recommendations are proposed investigations, not implemented outcomes.

## Verification

119,390 source rows retained; primary and foreign keys verified; dimension joins preserve row count; SQL totals reconcile to pandas for every month and hotel; no status/flag mismatches. The Excel source represents the complete dataset aggregated by arrival month, hotel and channel.
