-- Each diagnostic should return zero, unless stated otherwise.
SELECT 'orphan_hotel_rows' diagnostic,COUNT(*) issue_count
FROM bookings b LEFT JOIN hotels h ON h.hotel_id=b.hotel_id WHERE h.hotel_id IS NULL
UNION ALL
SELECT 'orphan_date_rows',COUNT(*) FROM bookings b LEFT JOIN dates d ON d.date_id=b.arrival_date WHERE d.date_id IS NULL
UNION ALL
SELECT 'invalid_outcome',COUNT(*) FROM bookings WHERE is_canceled NOT IN (0,1)
UNION ALL
SELECT 'status_flag_mismatch',COUNT(*) FROM bookings
WHERE (reservation_status='Check-Out' AND is_canceled<>0)
   OR (reservation_status IN ('Canceled','No-Show') AND is_canceled<>1);
