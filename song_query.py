from elasticsearch import Elasticsearch, helpers
from flask import Flask
import os
import json

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

app = Flask(__name__)

@app.route('/query')
def getSong():
    response = es.search(index='songs', body={"query": {"match": {"track_name": "Dance Monkey"}}})

if __name__ == '__main__':
    app.run(debug=True)
