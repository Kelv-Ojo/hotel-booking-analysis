# Reporting data dictionary

| Field | Meaning |
|---|---|
| source_row / booking_id | Original worksheet row number, used only as a technical record ID |
| hotel | City Hotel or Resort Hotel |
| is_canceled | Original 0/1 flag; no-shows also carry 1 |
| lead_time | Days between booking entry and arrival |
| arrival_date | Derived from source arrival year, month name and day |
| market_segment | Original marketing segment, with Undefined retained |
| distribution_channel | Original distribution channel, with Undefined retained |
| customer_type | Original customer category; not a guest identifier |
| deposit_type | Original deposit arrangement; not an intervention assignment |
| reservation_status | Canceled, Check-Out or No-Show |

Foreign-key dimensions contain distinct observed labels. Date dimension covers the complete consecutive arrival-date range. Missing/small groups are not invented. Aggregated cancellation rates always use summed numerators divided by summed denominators.
