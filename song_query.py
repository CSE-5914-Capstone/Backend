from elasticsearch import Elasticsearch, helpers
from flask import Flask
from flask_cors import CORS
import os
import json
import song_loader
import spotify_link
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))
    #Figure out how to get actual credentials loaded
clientId = '834545c65b434617a906b8ea321e7e5b'
clientPass = '8861fc75e1bd49c29aa035278faa6e8f'
authenticate = SpotifyOAuth(client_id=clientId,client_secret=clientPass, redirect_uri='http://127.0.0.1:5000/testLink')
sp = Spotify(client_credentials_manager=authenticate), authenticate
token = authenticate.get_access_token()
print('connection created')


def searchSimilar(targetSongData):
    #Some of the following variables are subject to change
    targetSubGenre = targetSongData['playlist_subgenre']
    targetDanceability = targetSongData['danceability']
    targetGenre = targetSongData['playlist_genre']
    targetEnergy = targetSongData['energy']
    targetKey = targetSongData['key']
    targetLoudness = targetSongData['loudness']
    targetLiveness = targetSongData['liveness']
    targetHappiness = targetSongData['valence']
    targetTempo = targetSongData['tempo']
    #{'match': {'playlist_subgenre' : targetSubGenre}}
    #{'match':{'key' : targetKey}}
    similarSongs = es.search(index='songs', body={'query': {'bool': {'must':[{'match':{'playlist_genre' : targetGenre}}],
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
    standInParams = dict()
    standInParams['track_name'] = 'Move Your Feet'
    return queryTop10(standInParams)

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