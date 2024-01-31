-- number_of_advertisements, ilość odtworzonych reklam w danym miesiącu
-- SELECT
--             user_id,
--             strftime('%Y', timestamp) as year,
--             strftime('%m', timestamp) as month,
--             COUNT(*) as number_of_advertisements
--         FROM
--             sessions
--         WHERE
--             event_type = 'advertisement'
--         GROUP BY
--             strftime('%Y', timestamp), strftime('%m', timestamp), user_id
--         ORDER BY
--             year, month

-- number_of_tracks, ilość przesłuchanych utworów w danym miesiącu
-- SELECT user_id,
--        strftime('%Y', timestamp) as year,
--        strftime('%m', timestamp) as month,
--        COUNT(DISTINCT track_id)  as number_of_tracks
-- FROM sessions
-- WHERE event_type = 'play'
-- GROUP BY user_id, strftime('%Y', timestamp), strftime('%m', timestamp)
-- ORDER BY year, month

-- number_of_skips, ilość pominiętych utworów w danym miesiącu
SELECT user_id,
       strftime('%Y', timestamp) as year,
       strftime('%m', timestamp) as month,
       COUNT(*)                  as number_of_skips
FROM sessions
WHERE event_type = 'skip'
GROUP BY user_id, strftime('%Y', timestamp), strftime('%m', timestamp)
ORDER BY year, month


-- number_of_likes, liczba danych lików w danym miesiącu
SELECT user_id,
       strftime('%Y', timestamp) as year,
       strftime('%m', timestamp) as month,
       COUNT(*)                  as number_of_likes

FROM sessions
WHERE event_type = 'like'
GROUP BY user_id, strftime('%Y', timestamp), strftime('%m', timestamp)
ORDER BY year, month

-- total_tracks_duration_ms, całkowity czas przesłuchanych utworów w danym miesiącu
SELECT
            user_id,
            strftime('%Y', timestamp) as year,
            strftime('%m', timestamp) as month,
            SUM(tracks.duration_ms) as total_tracks_duration_ms
        FROM
            sessions
        JOIN
            tracks ON sessions.track_id = tracks.id
        WHERE
            event_type = 'play'
        GROUP BY
            strftime('%Y', timestamp), strftime('%m', timestamp), user_id
        ORDER BY
            year, month

-- number_of_different_artists, ilość przesłuchanych artystów w danym miesiącu
SELECT
            user_id,
            strftime('%Y', timestamp) as year,
            strftime('%m', timestamp) as month,
            COUNT(DISTINCT artists.id) as number_of_different_artists
        FROM
            sessions
        JOIN
            tracks ON sessions.track_id = tracks.id
        JOIN
            artists ON tracks.id_artist = artists.id
        WHERE
            event_type = 'play'
        GROUP BY
            strftime('%Y', timestamp), strftime('%m', timestamp), user_id
        ORDER BY
            year, month


SELECT
    strftime('%Y', s.timestamp) AS year,
    strftime('%m', s.timestamp) AS month,
    s.user_id,
    AVG(strftime('%s', t.release_date)) AS average_release_date,
    AVG(t.duration_ms) AS average_duration_ms,
    AVG(CAST(t.explicit AS FLOAT)) AS explicit_tracks_ratio,
    AVG(t.popularity) AS average_popularity,
    AVG(t.acousticness) AS average_acousticness,
    AVG(t.danceability) AS average_danceability,
    AVG(t.energy) AS average_energy,
    AVG(t.instrumentalness) AS average_instrumentalness,
    AVG(t.liveness) AS average_liveness,
    AVG(t.loudness) AS average_loudness,
    AVG(t.speechiness) AS average_speechiness,
    AVG(t.tempo) AS average_tempo,
    AVG(t.valence) AS average_valence
FROM
    sessions s
JOIN
    tracks t ON s.track_id = t.id
WHERE
    s.event_type = 'play'
GROUP BY
    year, month, s.user_id
ORDER BY
    year, month, s.user_id;