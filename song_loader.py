from elasticsearch import Elasticsearch, helpers
import os
import json

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

# kaggle datasets download -d joebeachcaptial/30000-spotify-songs

with open("init_songs.json") as file:
    songs = json.loads(file.read())

if not es.indices.exists(index='songs'):
    print('Created blank index "songs"')
    es.indices.create(index='songs')

for song in songs:
    response = es.search(index='songs', body={"query": {"match_phrase": {"track_name": song['track_name']}}})
    if response['hits']['total']['value'] == 0:
        es.index(index='songs',body = song)


response = es.search(index='songs', body={"query": {"match": {"track_name": "Dance Monkey"}}})
print(response)


