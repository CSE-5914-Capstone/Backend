# Melody Miners Playlist Recommendation System Backend

## Engine for querying elasticsearch with song data

Provided here is the code to fill an existing elasticsearch docker container with songs from Spotify and create a playlist based on a requested song and tuning parameters from the [Melody Miners Frontend](https://github.com/CSE-5914-Capstone/frontend).

This docker container must be configured locally in order for songs to be indexed and searched. We recommend using Docker Desktop for simpler packaging and bootup of the instance for on-the-fly usage once installed and configured, but following the command line instructions from [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) to intialize the container.

Install [Docker Desktop](https://docs.docker.com/desktop/) for your local system if you currently do not have Docker. Then follow the above Elasticsearch install instructions. Optional step 4 is not needed for the Melody Miners system. Pay special attention to steps 5 and 7 to access and store certification information that will be needed in order to run the application. 

**Step 5**

The command line output following the issued command will be verbose, but a 20-character, plaintext, alphanumeric password is generated and highlighted after completion. Copy this text and save it to a file named `docker_elastic_pwd.txt` in the same directory as the Backend code (on the same level as this `README.md` file). The following step 6 details how to regenerate this password if you lose access to it. The kibana enrollment token can be ignored, as the actual application is local to your Docker container.

**Step 7**

This step accesses the certification file for Elastic that allows communication with your container from code. If you issue the command from a terminal located in the Backend directory, this certification file will be copied to the correct place. Otherwise, replace the `.` at the end of the command with the location of your Backend directory to put the certification in the correct location. 

At this point, to begin communicating with your elasticsearch instance, start the `es01` container on Docker via the desktop GUI or command line if comfortable. This is a simple press of a start button on Docker Desktop. 


### Accessing Data

Download [`uniquesongs.json`](https://drive.google.com/file/d/1aC2wqYVMMvoN8aLnbU5FxlkQ3LR0pIjE/view?usp=drive_link) for prepackaged song data. Add this file to the `datastore` directory (it is included in the .gitignore to prevent tracking of massive files). Run `temp_song_deleter.py` to assert that you have a clean elasticsearch index, and run `song_query.py` to open flask server.

**With the running Flask server, follow the instructions on the Melody Miners Frontend in order to begin generating playlists for your favorite songs!**

### Resetting

Run `temp_song_deleter.py` to clear current status of songs in index and songs index to reset workflow

## Extra Information

### Queryable API Routes

`/querycard`

The /querycard route is the default endpoint that is spun up by `song_query.py` and the corresponding flask server. This is the route that accepts specified song attributes to create a more user-specific playlist. The URL arguments available on this route are listed below.

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

### Elasticsearch Query Information

Query Matches:
  - Danceability Range +/- 0.15
  - Energy Range +/- 0.15
  - Loudness Range +/- 15
  - Liveness Range +/- 0.15
  - Happiness (Valence) Range +/- 0.15
  - Tempo Range +/- 15

Playlist will return songs that minimize the differences between song and target song attributes within this window. For example, a song with all slightly different attributes will be preferred over one that exact matches danceability and is nowhere near other attributes that the user specifies/are implied by the target song.
