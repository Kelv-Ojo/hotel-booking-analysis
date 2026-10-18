WITH performance AS (
 SELECT h.hotel,s.segment,c.channel,COUNT(*) bookings,
        SUM(b.is_canceled) canceled,AVG(b.lead_time) mean_lead_time_days
 FROM bookings b
 JOIN hotels h ON h.hotel_id=b.hotel_id
 JOIN segments s ON s.segment_id=b.segment_id
 JOIN channels c ON c.channel_id=b.channel_id
 GROUP BY h.hotel,s.segment,c.channel
 HAVING COUNT(*)>=100
)
SELECT *, ROUND(100.0*canceled/bookings,2) cancellation_pct,
       DENSE_RANK() OVER (PARTITION BY hotel ORDER BY 1.0*canceled/bookings DESC) risk_rank
FROM performance ORDER BY hotel,risk_rank;
