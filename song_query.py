from elasticsearch import Elasticsearch, helpers
from flask import Flask, request
from flask_cors import CORS
import os
import json
import song_loader
import normalize_parameters

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

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
    playlist['playlist'] = names
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
    return queryTop10(standInParams)

@app.route('/')
def init():

    if not es.indices.exists(index='songs'):
        song_loader.load_all()
    return ({"Songs": "Loaded"})

if __name__ == '__main__':
    init()
    app.run(debug=True)