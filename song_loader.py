from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
import json
import time

def load_all():
    elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
    elastic_pwd = elastic_pwd_file.read()
    elastic_pwd_file.close()

    es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

    # kaggle datasets download -d joebeachcaptial/30000-spotify-songs

    start = time.time()

    with open("backend/datastore/uniquesongs.json", encoding='utf8') as file:
        songs = json.loads(file.read())

    if not es.indices.exists(index='songs'):
        print('Created blank index "songs"')
        es.indices.create(index='songs')

    bulk(es, songs, index='songs')

    end = time.time()

    print(f"Loading {len(songs)} songs took {end-start} seconds ({(end-start)/60} minutes)")

    start = time.time()
    response = es.search(index='songs', body={"query": {"match": {"track_name": "Dance Monkey"}}})
    end=time.time()

    print(f"Single song search took {end-start} seconds ({(end-start)/60} minutes)")
