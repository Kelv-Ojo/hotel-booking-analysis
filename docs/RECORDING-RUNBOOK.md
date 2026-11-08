# Three-minute hotel case study recording

Prepared materials are complete. The personal recording is not complete: Kelvin needs to rehearse, record his own narration/screen and approve the final take. Do not describe the recording as published until a working video link exists.

## Before recording

Use the existing verified monthly outputs; do not refresh the dataset during the recording. Open the repository README, assets/screenshots/peak-month-2016.png, reports/peak_month_2016.json and docs/PEAK-MONTH-CASE-STUDY.md. Close private tabs, notifications and university documents. A webcam is optional. Record a brief audio check before starting. Record at 1080p if the recorder supports it, with readable chart labels and no background music required.

Reproduce the small analysis with `python src/peak_month_review.py`. To rebuild the chart, install matplotlib and run `python src/plot_peak_month.py`; the plot reads the same monthly output and checks twelve months per hotel and status reconciliation.

## Suggested narration and screen sequence

Rehearse at a natural pace and trim pauses to approximately three minutes. These are cue targets, not a claim that a video has already been timed.

**0:00–0:30 — README and business question**

“I’m Kelvin. This case study asks which arrival month had the most bookings, and whether that peak is enough evidence to change hotel staffing. I used an existing historical dataset from two Portuguese hotels. The full snapshot has 119,390 booking records, but this comparison uses only 2016. That is the only complete arrival year in the snapshot, so it avoids comparing a full year with the partial years on either side.”

**0:30–1:15 — Chart and definitions**

“This chart shows scheduled arrival month, rather than when someone made the reservation or when its status changed. Each bar is split into checked-out records and cancellation flags. Cancellation flags include no-shows. These definitions matter: a booking is not the same thing as an occupied room-night. I checked that each hotel has twelve distinct monthly observations, and that the two status counts add back to the booking total. The underlying analysis also preserves source row identifiers and reconciles SQL joins against Python aggregates.”

**1:15–2:00 — October results and JSON**

“October had the highest booking count for both hotels. City Hotel had 4,219 bookings: 2,272 checked-out records and 1,947 cancellation flags. Resort Hotel had 1,984 bookings: 1,417 checked-out records and 567 cancellation flags. Those are observed counts from this dataset. The larger City Hotel booking peak does not translate directly into the same number of realised stays. This is why I would show both the total and its status breakdown to a decision maker, rather than relying on a single headline number.”

**2:00–2:40 — Practical recommendation**

“My recommendation is to investigate the peak before changing staffing levels. I would ask for occupied room-nights, staffing schedules, hotel capacity and the timing of cancellations, then compare service demand with available staff. I would also check whether events or customer and channel mix explain the pattern. This analysis does not estimate a causal effect, forecast future demand or demonstrate a financial saving. It identifies where a hotel team could ask better operational questions.”

**2:40–3:00 — Reproduction and close**

“The repository includes the source attribution, SQL, Python analysis, checked results and a reproducible command for this comparison. My main takeaway is that a useful dashboard connects a clear question to a consistent date definition and a reconciled denominator. The next decision needs operational evidence beyond booking counts. Thank you.”

## Final take acceptance

- Check that all spoken counts match the JSON and the chart is readable.
- Keep the caveats about arrival dates, cancellation flags, partial years and staffing evidence.
- Ensure the recording is close to three minutes and audio is understandable.
- Watch the exported file from start to end; remove private information before uploading.
- Supply or approve a public/unlisted video destination and a working link. Add that link to the case study and board, then verify playback before marking the recording requirement Done.
