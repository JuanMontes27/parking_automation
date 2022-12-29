DROP TABLE IF EXISTS vehicle_types;
DROP TABLE IF EXISTS vehicles;

CREATE TABLE vehicle_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type TEXT UNIQUE NOT NULL,
    payment REAL NOT NULL
);

INSERT INTO vehicle_types (vehicle_type, payment) VALUES ("Oficial", 0.0), ("Residente", 1.0), ("No residente", 3.0);

CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type_id INTEGER NOT NULL,
    plate_number TEXT NOT NULL,
    date_start TEXT,
    date_end TEXT,
    parked_time TEXT,
    payment_parking REAL,
    FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_types (id)
);