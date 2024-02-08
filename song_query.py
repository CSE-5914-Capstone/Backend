from elasticsearch import Elasticsearch, helpers
from flask import Flask
import os
import json
import song_loader

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

def searchSimilar(targetSongData):
    targetSubGenre = targetSongData['playlist_subgenre']
    targetDanceability = targetSongData['danceability']
    similarSongs = es.search(index='songs', body={'query': {'bool': {'must':[{'match': {'playlist_subgenre' : targetSubGenre}}, {'match':{'danceability': targetDanceability}}]}}})
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

@app.route('/query')
def getSong():
    standInParams = dict()
    standInParams['track_name'] = 'Macarena'
    return queryTop10(standInParams)

@app.route('/')
def init():

    if not es.indices.exists(index='songs'):
        song_loader.load_all()
    return ({"Songs": "Loaded"})

if __name__ == '__main__':
    init()
    app.run(debug=True)
