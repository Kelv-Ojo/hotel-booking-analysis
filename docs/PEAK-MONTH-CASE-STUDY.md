# Which 2016 arrival month had the most bookings?

This is a new question within the existing hotel project, using the complete 2016 arrival year. It measures historical bookings, not occupied room-nights, reservation-creation dates or future demand. Reproduce with `python src/peak_month_review.py`; results are in reports/peak_month_2016.json.

Both hotels peak in October: City Hotel has 4,219 bookings, including 1,947 cancellation flags and 2,272 checked-out records; Resort Hotel has 1,984, including 567 cancellation flags and 1,417 checked-out records. Annual bookings are 38,140 and 18,567 respectively. The script checks 12 unique months per hotel and status reconciliation. The cancellation flag includes no-shows; no causal or occupancy inference is made.

Before proposing staffing changes, compare realised arrivals and room-night demand with staffing, capacity and calendar-event data. A booking peak alone does not establish labour demand. No staffing saving is claimed.

## Three-minute walkthrough script

0:00–0:30: Introduce the question and explain why 2016 is the only complete arrival year in this snapshot.

0:30–1:15: Show monthly.csv, the per-hotel month counts and the status-reconciliation checks. Explain that dates refer to arrival month.

1:15–2:00: Run the script and compare October booking totals with checked-out records. Explain why cancellation flags change the interpretation.

2:00–2:40: Explain the proposed next decision: gather occupancy, capacity and staffing data before choosing staffing levels.

2:40–3:00: State limits, show source/reproduction links, and invite questions.

Recording status: a script is prepared; no personal walkthrough has been recorded or claimed. Kelvin must supply or record the presentation to complete that board requirement.
