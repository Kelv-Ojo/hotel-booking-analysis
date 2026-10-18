-- One-to-many dimension joins preserve one row per original booking.
WITH monthly AS (
 SELECT d.year_month, h.hotel, COUNT(*) bookings,
        SUM(b.is_canceled) canceled,
        SUM(CASE WHEN b.reservation_status='Check-Out' THEN 1 ELSE 0 END) checked_out,
        SUM(CASE WHEN b.reservation_status='No-Show' THEN 1 ELSE 0 END) no_shows
 FROM bookings b
 JOIN dates d ON d.date_id=b.arrival_date
 JOIN hotels h ON h.hotel_id=b.hotel_id
 GROUP BY d.year_month,h.hotel
), rates AS (
 SELECT *, 1.0*canceled/bookings cancellation_rate,
        LAG(bookings) OVER (PARTITION BY hotel ORDER BY year_month) previous_month_bookings
 FROM monthly
)
SELECT *, ROUND(100.0*(bookings-previous_month_bookings)/NULLIF(previous_month_bookings,0),2) booking_change_pct
FROM rates ORDER BY year_month,hotel;
