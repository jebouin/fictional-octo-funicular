// Create a keyspace for a single data center and no replication
CREATE KEYSPACE app WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

// Use this keyspace
USE app;

// Create a table to store the measurements
CREATE TABLE IF NOT EXISTS measurements (
    id uuid,                             // A unique identifier for the measurement
    station_id uuid,                     // Another unique identifier for the weather station
    latitude float,                      // The GPS coordinates of the measurement
    longitude float, 
    time timestamp,                      // The time and date of the measurement
    temperature float,                   // The temperature in Celsius
    humidity float,                      // The humidity from 0 to 100
    PRIMARY KEY (station_id, time)       // Partition the measurements by station id and cluster by time
) WITH CLUSTERING ORDER BY (time ASC);

// Insert some measurements from 2 different stations
INSERT INTO measurements (
    id, 
    station_id, 
    latitude, 
    longitude, 
    time, 
    temperature, 
    humidity
) VALUES (
    uuid(), 
    b8fbdab0-f7d4-49c7-b46a-a621368e007e,
    30.5803685, 
    20.3492659, 
    '2018-10-19T12:24:34+00:00', 
    20, 
    92
);
INSERT INTO measurements (
    id, 
    station_id, 
    latitude, 
    longitude, 
    time, 
    temperature, 
    humidity
) VALUES (
    uuid(), 
    b8fbdab0-f7d4-49c7-b46a-a621368e007e,
    30.5803685, 
    20.3492659, 
    '2018-10-19T12:23:34+00:00', 
    19, 
    80
);
INSERT INTO measurements (
    id, 
    station_id, 
    latitude, 
    longitude, 
    time, 
    temperature, 
    humidity
) VALUES (
    uuid(), 
    b8fbdab0-f7d4-49c7-b46a-a621368e007e,
    30.5803685, 
    20.3492659, 
    '2018-10-19T12:25:34+00:00', 
    22, 
    88
);
INSERT INTO measurements (
    id, 
    station_id, 
    latitude, 
    longitude, 
    time, 
    temperature, 
    humidity
) VALUES (
    uuid(), 
    b8fbdab0-f7d4-49c7-b46a-a621368e007e,
    30.5803685, 
    20.3492659, 
    '2018-10-19T17:10:34+00:00', 
    18, 
    42
);
INSERT INTO measurements (
    id, 
    station_id, 
    latitude, 
    longitude, 
    time, 
    temperature, 
    humidity
) VALUES (
    uuid(), 
    d2cf81fe-a003-4a38-a379-e0baa98461de,
    51.95678134,
    4.06228767,
    '2018-10-19T08:24:34+00:00', 
    2, 
    51
);

// Select every measurement from a given station
SELECT latitude, longitude, time, temperature, humidity FROM measurements WHERE station_id = b8fbdab0-f7d4-49c7-b46a-a621368e007e;

// Select every measurement from a given station between 12:24 and 12:30
SELECT latitude, longitude, time, temperature, humidity FROM measurements WHERE station_id = b8fbdab0-f7d4-49c7-b46a-a621368e007e AND time >= '2018-10-19T12:24:00+00' AND time <= '2018-10-19T12:30:00+00';
