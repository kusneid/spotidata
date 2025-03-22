{{ config(
    materialized='table',
    alias='tracks'
) }}

WITH cleaned_tracks AS (
    SELECT track_name, artist, popularity, lyrics
    FROM {{ source('default', 'tracks') }}
    WHERE track_name NOT LIKE '%(feat%'
      AND length(lyrics) > 0
)
SELECT *
FROM cleaned_tracks
