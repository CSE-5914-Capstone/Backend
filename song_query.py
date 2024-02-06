from elasticsearch import Elasticsearch, helpers
from flask import Flask
import os
import json

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

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
    similarSongs = es.search(index='songs', body={'query': {'bool': {'must':[{'match': {'playlist_subgenre' : targetSubGenre}}, {'match':{'danceability': targetDanceability}}, {'match':{'playlist_genre' : targetGenre}}, {'match':{'energy' : targetEnergy}}, {'match':{'key' : targetKey}}, {'match':{'loudness' : targetLoudness}}, {'match':{'liveness' : targetLiveness}}, {'match':{'valence': targetHappiness}}, {'match':{'tempo' : targetTempo}}]}}})
    return similarSongs['hits']['hits']

def queryTop10(standInParams):
    trackname = standInParams['track_name']
    targetSong = es.search(index='songs', body={"query": {"match": {"track_name": trackname}}})['hits']['hits'][0]
    targetSongData = targetSong['_source']

    names = []
    similarSongs = searchSimilar(targetSongData)
    for song in similarSongs:
        names.append(song['_source']['track_name'])
    return names
    

app = Flask(__name__)

@app.route('/query')
def getSong():
    standInParams = dict()
    standInParams['track_name'] = 'Macarena'
    return queryTop10(standInParams)

if __name__ == '__main__':
    print(getSong())
    #app.run(debug=True)
