CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(100),
email VARCHAR(100) UNIQUE,
password VARCHAR(255),
role VARCHAR(30)
);

CREATE TABLE parking_lots(
id INTEGER PRIMARY KEY AUTOINCREMENT,
parking_name VARCHAR(100),
location VARCHAR(150),
total_slots INTEGER,
available_slots INTEGER,
status VARCHAR(20)
);

CREATE TABLE vehicle_entries(
id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_id INTEGER,
parking_id INTEGER,
vehicle_number VARCHAR(30) UNIQUE,
vehicle_type VARCHAR(30),
entry_time DATETIME,
exit_time DATETIME,
slot_number INTEGER,
parking_fee FLOAT,
FOREIGN KEY(customer_id) REFERENCES users(id),
FOREIGN KEY(parking_id) REFERENCES parking_lots(id)
);

CREATE TABLE payments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
entry_id INTEGER UNIQUE,
amount FLOAT,
payment_method VARCHAR(30),
payment_status VARCHAR(20),
FOREIGN KEY(entry_id) REFERENCES vehicle_entries(id)
);
