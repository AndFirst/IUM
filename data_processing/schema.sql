CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    street TEXT,
    favourite_genres TEXT,
    premium_user BOOLEAN
);

CREATE TABLE IF NOT EXISTS artists (
    id TEXT PRIMARY KEY,
    name TEXT,
    genres TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
    id TEXT PRIMARY KEY,
    name TEXT,
    popularity INTEGER,
    duration_ms INTEGER,
    explicit INTEGER,
    id_artist TEXT,
    release_date DATE,
    danceability REAL,
    energy REAL,
    key INTEGER,
    mode INTEGER,
    loudness REAL,
    speechiness REAL,
    acousticness REAL,
    instrumentalness REAL,
    liveness REAL,
    valence REAL,
    tempo REAL,
    time_signature INTEGER,
    FOREIGN KEY (id_artist) REFERENCES artists(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER,
    timestamp TEXT,
    user_id INTEGER,
    track_id TEXT,
    event_type TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

CREATE TABLE IF NOT EXISTS track_storage (
    track_id TEXT PRIMARY KEY,
    storage_class TEXT,
    daily_cost REAL,
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);