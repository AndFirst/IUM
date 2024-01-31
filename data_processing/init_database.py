from concurrent.futures import ThreadPoolExecutor
import sqlite3
import json

ARTIST_PATH = 'data/v4/artists.jsonl'
SESSION_PATH = 'data/v4/sessions.jsonl'
TRACK_STORAGE_PATH = 'data/v4/track_storage.jsonl'
TRACKS_PATH = 'data/v4/tracks.jsonl'
USERS_PATH = 'data/v4/users.jsonl'

DATABASE_PATH = 'database.db'


def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    return data


def reset_database():
    query = '''
    DROP TABLE IF EXISTS ARTISTS;
    DROP TABLE IF EXISTS SESSIONS;
    DROP TABLE IF EXISTS TRACK_STORAGE;
    DROP TABLE IF EXISTS TRACKS;
    DROP TABLE IF EXISTS USERS;
    '''

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executescript(query)
    conn.commit()
    conn.close()


def init_schema():
    with open('data_processing/schema.sql', 'r') as file:
        schema = file.read()
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


def load_users():
    data = load_jsonl(USERS_PATH)

    query = '''
        INSERT INTO users (user_id, name, city, street, favourite_genres, premium_user)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executemany(query, [(user['user_id'], user['name'], user['city'], user['street'],
                                json.dumps(user.get('favourite_genres', [])), user.get('premium_user')) for user in
                               data])
    conn.commit()
    conn.close()


def load_tracks():
    data = load_jsonl(TRACKS_PATH)

    query = '''
    INSERT INTO tracks (
        id, name, popularity, duration_ms, explicit, id_artist, release_date,
        danceability, energy, key, mode, loudness, speechiness, acousticness,
        instrumentalness, liveness, valence, tempo, time_signature
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executemany(query, [
        (
            track['id'], track['name'], track['popularity'], track['duration_ms'],
            track['explicit'], track['id_artist'], track['release_date'],
            track['danceability'], track['energy'], track['key'], track['mode'],
            track['loudness'], track['speechiness'], track['acousticness'],
            track['instrumentalness'], track['liveness'], track['valence'],
            track['tempo'], track['time_signature']
        ) for track in data
    ])
    conn.commit()
    conn.close()


def load_track_storage():
    data = load_jsonl(TRACK_STORAGE_PATH)

    query = '''
    INSERT INTO track_storage (
    track_id, storage_class, daily_cost
    ) VALUES (?, ?, ?)
    '''

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executemany(query, [
        (track_storage['track_id'], track_storage['storage_class'], track_storage['daily_cost']) for track_storage in
        data
    ])
    conn.commit()
    conn.close()


def load_artists():
    data = load_jsonl(ARTIST_PATH)

    query = '''
    INSERT INTO artists 
    (id, name, genres) 
    VALUES (?, ?, ?)
    '''

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executemany(query, [(artist['id'], artist['name'], json.dumps(
        artist['genres'])) for artist in data])
    conn.commit()
    conn.close()


# Zakładam, że masz zdefiniowaną funkcję load_jsonl
# def load_jsonl(path):
#     ...


def insert_batch(cursor, data_batch):
    query = '''
        INSERT INTO sessions (
            session_id, timestamp, user_id, track_id, event_type
        ) VALUES (?, ?, ?, ?, ?)
    '''
    cursor.executemany(query, data_batch)


def load_sessions():
    data = load_jsonl(SESSION_PATH)
    batch_size = 1000  # Dobierz rozmiar batcha odpowiedni do Twoich danych

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        with conn, ThreadPoolExecutor() as executor:
            cursor = conn.cursor()
            futures = []

            for i in range(0, len(data), batch_size):
                data_batch = data[i:i + batch_size]
                future = executor.submit(insert_batch, cursor, data_batch)
                futures.append(future)

            # Oczekiwanie na zakończenie wszystkich zadań
            for future in futures:
                future.result()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    reset_database()
    init_schema()
    load_users()
    load_tracks()
    load_track_storage()
    load_artists()
    # load_sessions()
    pass
