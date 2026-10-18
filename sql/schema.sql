PRAGMA foreign_keys = ON;
CREATE TABLE hotels (hotel_id INTEGER PRIMARY KEY, hotel TEXT NOT NULL UNIQUE);
CREATE TABLE channels (channel_id INTEGER PRIMARY KEY, channel TEXT NOT NULL UNIQUE);
CREATE TABLE segments (segment_id INTEGER PRIMARY KEY, segment TEXT NOT NULL UNIQUE);
CREATE TABLE dates (date_id TEXT PRIMARY KEY, year INTEGER NOT NULL, month INTEGER NOT NULL, year_month TEXT NOT NULL);
CREATE TABLE bookings (
 booking_id INTEGER PRIMARY KEY,
 hotel_id INTEGER NOT NULL REFERENCES hotels(hotel_id),
 channel_id INTEGER NOT NULL REFERENCES channels(channel_id),
 segment_id INTEGER NOT NULL REFERENCES segments(segment_id),
 arrival_date TEXT NOT NULL REFERENCES dates(date_id),
 is_canceled INTEGER NOT NULL CHECK(is_canceled IN (0,1)),
 lead_time INTEGER NOT NULL CHECK(lead_time>=0),
 customer_type TEXT NOT NULL,
 deposit_type TEXT NOT NULL,
 reservation_status TEXT NOT NULL
);
CREATE INDEX booking_arrival ON bookings(arrival_date);
CREATE INDEX booking_segment ON bookings(segment_id);
