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
import scale_value


elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))
    #Figure out how to get actual credentials loaded
clientId = '834545c65b434617a906b8ea321e7e5b'
clientPass = '8861fc75e1bd49c29aa035278faa6e8f'
authenticate = SpotifyOAuth(client_id=clientId,client_secret=clientPass, redirect_uri='http://127.0.0.1:5000/testLink')
#sp = Spotify(client_credentials_manager=authenticate), authenticate
#token = authenticate.get_access_token()
#print('connection created')


def makeParams(track_name, danceability, energy, loudness, liveness, valence, tempo):
    params = dict()
    params['danceability'] = scale_value.scale_danceability(danceability)
    params['energy'] = scale_value.scale_energy(energy)
    params['loudness'] = scale_value.scale_loudness(loudness)
    params['liveness'] = scale_value.scale_liveness(liveness)
    params['valence'] = scale_value.scale_valence(valence)
    params['tempo'] = scale_value.scale_tempo(tempo)

    if track_name is None:
        params['track_name'] = 'Macarena'
    else:
        params['track_name'] = track_name
    return params

def searchSimilar(targetSongData, userData):
    targetDanceability = targetSongData['danceability'] if userData['danceability'] == -1 else userData['danceability']
    targetEnergy = targetSongData['energy'] if userData['energy'] == -1 else userData['energy']
    targetLoudness = targetSongData['loudness'] if userData['loudness'] == -1 else userData['loudness']
    targetLiveness = targetSongData['liveness'] if userData['liveness'] == -1 else userData['liveness']
    targetHappiness = targetSongData['valence'] if userData['valence'] == -1 else userData['valence']
    targetTempo = targetSongData['tempo'] if userData['tempo'] == -1 else userData['tempo']
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
    similarSongs = searchSimilar(targetSongData, standInParams)
    for song in similarSongs:
        currsongdata = dict()
        currsongdata['track_name'] = song['_source']['track_name']
        currsongdata['track_id'] = song['_source']['track_id']
        currsongdata['spotify_link'] = 'https://open.spotify.com/track/' + song['_source']['track_id']
        currsongdata['tempo'] = int(song['_source']['tempo'])
        currsongdata['artists'] = song['_source']['artists']
        currsongdata['album_id'] = song['_source']['track_album_id']
        names.append(currsongdata)
    playlist = dict()
    playlist['Playlist'] = names
    return playlist

def getSongAttributes(standInParams):
    trackname = standInParams['track_name']
    targetSong = es.search(index='songs', body={"query": {"match": {"track_name": trackname}}})['hits']['hits'][0]
    targetSongData = targetSong['_source']

    standInParams = makeParams(trackname, None, None, None, None, None, None)
    names = []
    similarSongs = searchSimilar(targetSongData, standInParams)
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
        track_name = "Macarena"
    standInParams = dict()
    standInParams['track_name'] = f"{track_name}"

    standInParams = makeParams(track_name, None, None, None, None, None, None)
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

    return queryTop10(params)


@app.route('/testLink')
def outputLinks():
    params = dict()
    params['track_name'] = 'Move Your Feet'
    playlist = getSongAttributes(params)
    links = []
    #print(playlist)
    for song in playlist['Playlist Songs with attributes']:
        links.append('https://open.spotify.com/track/' + song['track_id'])
    #links['Song Links'] = spotify_link.setLinks(playlist, token, authenticate)
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
