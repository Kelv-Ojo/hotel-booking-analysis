# Explaining this case study in an interview

## A short explanation to practise

“I developed an existing hotel dashboard project into a reproducible cancellation analysis. I checked metric scope and dates, built a relational SQL model, and reconciled its results to an independent Python calculation. The Excel report makes it possible to compare hotel and channel performance without confusing partial years or averaging percentages.”

This project was developed with AI assistance. Review and run the code before describing individual choices as your own. Do not claim professional client experience, a deployed Power BI report or financial savings.

## Questions to be ready for

- Why keep duplicate-looking bookings? There is no source business booking ID proving they are duplicates; removing them could discard valid bookings.
- Why do dimension joins preserve totals? Dimension keys are unique and every fact row has exactly one match. Foreign-key and row-count checks verify this.
- Why not average cancellation rates? A group with ten bookings should not weigh as much as a group with ten thousand. Sum canceled counts and divide by summed bookings.
- Why do arrival and reservation-status dates differ? They describe different business events. All new comparisons consistently use arrival date.
- Is the cancellation rate causal? No. Hotel, channel, lead time and customer mix are confounded; investigate or run a controlled intervention before recommending a policy change.
- What would you do next? Validate reporting with a stakeholder, investigate high-volume channel/lead-time segments, and test confirmation messages while measuring incremental outcomes.

## Hands-on practice

Run the script, open one SQL query, explain each join, and independently check one month's count. Change the workbook filters and explain how the results change. Then add a question of your own and document the answer and its limitations.
