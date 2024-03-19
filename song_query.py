from elasticsearch import Elasticsearch, helpers
from flask import Flask, request
from flask_cors import CORS
import os
import json
import song_loader
import spotify_link
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import normalize_parameters


elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))
    #Figure out how to get actual credentials loaded
clientId = '834545c65b434617a906b8ea321e7e5b'
clientPass = '8861fc75e1bd49c29aa035278faa6e8f'
authenticate = SpotifyOAuth(client_id=clientId,client_secret=clientPass, redirect_uri='http://127.0.0.1:5000/testLink')
sp = Spotify(client_credentials_manager=authenticate), authenticate
token = authenticate.get_cached_token()
print('connection created')


def makeParams(track_name, danceability, energy, loudness, liveness, valence, tempo):
    params = dict()
    params['danceability'] = danceability
    params['energy'] = energy
    params['loudness'] = loudness
    params['liveness'] = liveness
    params['valence'] = valence
    params['tempo'] = tempo
    
    for key, value in params.items():
        if value is None:
            params[key] = -1

    if track_name is None:
        params['track_name'] = 'Macarena'
    else:
        params['track_name'] = track_name
    return params

def searchSimilar(targetSongData):
    #Some of the following variables are subject to change

    targetDanceability = targetSongData['danceability']
    targetEnergy = targetSongData['energy']
    targetLoudness = targetSongData['loudness']
    targetLiveness = targetSongData['liveness']
    targetHappiness = targetSongData['valence']
    targetTempo = targetSongData['tempo']
    similarSongs = es.search(index='songs', body={'query': {'bool': { #'must': [{'match':{'playlist_genre' : targetGenre}}],
                    'filter': [
                    {'range':{'danceability': {'gte': targetDanceability - 0.15, 'lte': targetDanceability + 0.15}}}, 
                    {'range':{'energy' : {'gte': targetEnergy - 0.15, 'lte': targetEnergy + 0.15}}},  
                    {'range':{'loudness' : {'gte': targetLoudness - 15, 'lte': targetLoudness + 15}}}, 
                    {'range':{'liveness' : {'gte': targetLiveness - 0.15, 'lte': targetLiveness + 0.15}}}, 
                    {'range':{'valence': {'gte': targetHappiness - 0.15, 'lte': targetHappiness + 0.15}}}, 
                    {'range':{'tempo' : {'gte': targetTempo - 15, 'lte': targetTempo + 15}}}
                    ]}}})
    return similarSongs['hits']['hits']

def queryTop10(standInParams):
    trackname = standInParams['track_name']
    targetSong = es.search(index='songs', body={"query": {"match": {"track_name": trackname}}})['hits']['hits'][0]
    targetSongData = targetSong['_source']

    names = []
    similarSongs = searchSimilar(targetSongData)
    for song in similarSongs:
        names.append(song['_source']['track_name'])
    playlist = dict()
    playlist['Playlist'] = names
    return playlist

def getSongAttributes(standInParams):
    trackname = standInParams['track_name']
    targetSong = es.search(index='songs', body={"query": {"match": {"track_name": trackname}}})['hits']['hits'][0]
    targetSongData = targetSong['_source']

    names = []
    similarSongs = searchSimilar(targetSongData)
    for song in similarSongs:
        names.append(song['_source'])
    #print(names)
    playlist = dict()
    playlist['Playlist Songs with attributes'] = names
    return playlist
    

app = Flask(__name__)
CORS(app)

@app.route('/query')
def getSong():
    track_name = request.args.get('trackname')
    if track_name is None:
        track_name = "Move Your Feet"
    standInParams = dict()
    standInParams['track_name'] = f"{track_name}"
    return queryTop10(standInParams)


@app.route('/querycard')
def getSongAndAttributes():
    track_name = request.args.get('trackname')
    danceability = request.args.get('danceability')
    energy = request.args.get('energy')
    loudness = request.args.get('loudness')
    liveness = request.args.get('liveness')
    valence = request.args.get('valence')
    tempo = request.args.get('tempo')

    params = makeParams(track_name, danceability, energy, loudness, liveness, valence, tempo)


@app.route('/testLink')
def outputLinks():
    params = dict()
    params['track_name'] = 'Move Your Feet'
    playlist = getSongAttributes(params)
    links = []
    #print(playlist)
    for song in playlist['Playlist Songs with attributes']:
        newObj = dict()
        newObj['Song Name'] = (song['track_name'])
        #newObj['Artist'] = (song['track_artist'])
        newObj['Link'] = ('https://open.spotify.com/track/' + song['track_id'])
        links.append(newObj)
    #links = spotify_link.setLinks(playlist, authenticate, token)
    linkPlaylist = dict()
    linkPlaylist['Song Links'] = links
    return linkPlaylist


@app.route('/')
def init():

    if not es.indices.exists(index='songs'):
        song_loader.load_all()
    return ({"Songs": "Loaded"})

if __name__ == '__main__':
    init()
    app.run(debug=True)
