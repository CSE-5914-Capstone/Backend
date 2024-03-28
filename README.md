# Engine for querying elasticsearch with song data

Copy `http_ca.crt` to directory and make a text file called `docker_elastic_pwd.txt` with your docker elastic password.
Those are in the .gitignore file, keep your local versions local

### Accessing Data

Download [`track_features.csv`](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs) from https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs. Add this file to the `datastore` directory (it is included in the .gitignore to prevent tracking of massive files). Run `csvtojson.py` in order to get the data into json format, run `clean_data.py` to create the unique song data which will eventually be indexed, run `temp_song_deleter.py` to assert that you have a clean elasticsearch index, and run `song_query.py` to open flask server.

The /init route answers requests with a simple object that states that songs have been loaded.

The /query route answers requests with 10 an array of 10 song names constituting a playlist. A `?trackname=<insert song name>` parameter can be supplied to query for a specific song, but if no song is supplied, the default playlist returned is for The Macarena.

### Resetting

Run `temp_song_deleter.py` to clear current status of songs in index and songs index to reset workflow

## Queryable API Routes

`\querycard`

**All params scale from 0-10 to range of values available in data**
- Parameters 
  - `?trackname`: plaintext optional name of a song
    - defaults to 'Macarena'
  - `?danceability`: 0-10 user specified level of song danceability
    - defaults to `trackname` danceability value
  - `?energy`: 0-10 user specified level of song energy
    - defaults to `trackname` energy value
  - `?loudness`: 0-10 user specified level of song loudness
    - defaults to `trackname` loudness value
  - `?liveness`: 0-10 user specified level of song liveness
    - defaults to `trackname` loudness value
  - `?valence`: 0-10 user specified level of song valence (spotify uses this score to capture "happiness" of a song)
    - defaults to `trackname` loudness value
  - `?tempo`: 0-10 user specified tempo of a song
    - defaults to `trackname` tempo (bpm)

Returns object for a playlist on that track name

```
{"Playlist":[
  {
    "album_id": string,
    "artists":[
        string,
        string,
      ...
      ],
    "spotify_link": string,
    "tempo": float,
    "track_id": string,
    "track_name": string
  },
  {
    ...
  },
  ...
]}
```

`\query`

- Parameters
  - `?trackname`: plaintext optional name of a song 
    - defaults to 'Macarena'
    - playlist based on this song and its attributes

Returns object for a playlist on that track name

```
{"Playlist":[
  {
    "album_id": string,
    "artists":[
        string,
        string,
      ...
      ],
    "spotify_link": string,
    "tempo": float,
    "track_id": string,
    "track_name": string
  },
  {
    ...
  },
  ...
]}
```

`\testLink`

- Returns an object with key `Song Links` and a value of 10 links to songs on spotify
  - Creates on song name "Move your Feet"

- Fairly deprecated route, no need to hit it

```
{"Song Links":[
  spotify link string,
  spotify link string,
  ...
]}
```

## Data dictionary - Songs
`track_id` - Hash for song

`track_name` - Title of song

`track_artist` - Title artist

`track_album_id` - Hash for song's listed album

`danceability` - 0-1 score for danceability 

`energy` - 0-1 score for energy

`loudness` - -46.2-1.27 score for decibels of song compared to some average Spotify defines

`liveness` - 0-1 score for presence of an audience in track sound

`valence` - 0-1 score for happiness of a track

`tempo` - Beats per Minute of the track

`duration_ms` - Time of track in milliseconds

`explicit` - Binary flag for explicitness of a song

## Query Information
Current Input - route `query?trackname=<enter song here>`. This will return a 10 song playlist 
Query Matches:
  - Genre of search song to the queried songs
Query Filter:
  - Danceability Range +/- 0.15
  - Energy Range +/- 0.15
  - Loudness Range +/- 15
  - Liveness Range +/- 0.15
  - Happiness (Valence) Range +/- 0.15
  - Tempo Range +/- 15

