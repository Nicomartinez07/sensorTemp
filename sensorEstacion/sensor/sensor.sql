CREATE TABLE IF NOT EXISTS Sensores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        temperature REAL,
        humidity REAL, 
        pressure REAL, 
        lightLevel REAL,
        waterLevel REAL,
        sunrise TEXT,
        sunset TEXT
    )