from elasticsearch import Elasticsearch, helpers
import os
import json
import time

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

# kaggle datasets download -d joebeachcaptial/30000-spotify-songs

start = time.time()

with open("initsongs_30000.json", encoding='utf8') as file:
    songs = json.loads(file.read())

if not es.indices.exists(index='songs'):
    print('Created blank index "songs"')
    es.indices.create(index='songs')

inc = 0
for song in songs:
    response = es.search(index='songs', body={"query": {"match_phrase": {"track_id": song['track_id']}}})
    if response['hits']['total']['value'] == 0:
        es.index(index='songs',body = song)
    inc = inc+1
    if(inc%500 == 0):
        print(f'{inc} songs loaded')

end = time.time()

print(f"Loading {inc} songs took {end-start} seconds ({(end-start)/60} minutes)")

start = time.time()
response = es.search(index='songs', body={"query": {"match": {"track_name": "Dance Monkey"}}})
print(response)
end=time.time()

print(f"Single song search took {end-start} seconds ({(end-start)/60} minutes)")

