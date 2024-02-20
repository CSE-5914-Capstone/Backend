# Engine for querying elasticsearch with song data

Copy `http_ca.crt` to directory and make a text file called `docker_elastic_pwd.txt` with your docker elastic password.
Those are in the .gitignore file, keep your local versions local

Run `song_loader.py` to load 30000 song test set and query based on pre loaded query in file
- Modify the query on line 37 of that file to test for different returns
- Working on `song_query.py` to modularize elasticsearch engine

Run `temp_song_deleter.py` to clear current status of songs in index and songs index to reset workflow

## Data dictionary - Songs
`track_id` - Hash for song
`track_name` - Title of song
`track_artist` - Title artist
`track_popularity` - 0-100 popularity score
`track_album_id` - Hash for song's listed album
`track_album_name` - Associated album title
`track_album_release_date` - Associated album release date
`playlist_name` - Name of playlist song was pulled from
`playlist_id` - Hash for playlist song was pulled from
`playlist_genre` - Genre of song's playlist
`playlist_subgenre` - More granular genre of playlist song pulled from
`danceability` - 0-1 score for danceability 
`energy` - 0-1 score for energy
`key` - 0-11 indicator for pitch key of song
`loudness` - -46.2-1.27 score for decibels of song compared to some average Spotify defines
`mode` - Binary flag (0 for minor key, 1 for major key)
`speechiness` - 0-1 score for percentage of track that is spoken words
`acousticness` - 0-1 score for confidence in guess that track is acoustic
`instrumentalness` - 0-1 prediction score for if track has vocals
`liveness` - 0-1 score for presence of an audience in track sound
`valence` - 0-1 score for happiness of a track
`tempo` - Beats per Minute of the track
`duration_ms` - Time of track in milliseconds

## Query Information
Current Input - One hard-coded track name.
Query Matches:
  - Genre of search song to the queried songs
Query Filter:
  - Danceability Range +/- 0.15
  - Energy Range +/- 0.15
  - Loudness Range +/- 15
  - Liveness Range +/- 0.15
  - Happiness (Valence) Range +/- 0.15
  - Tempo Range +/- 15

