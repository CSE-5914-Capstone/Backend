from elasticsearch import Elasticsearch, helpers
import os
import json

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

def normalizeDanceability():
    return 0

def normalizeEnergy():
    return 0

def normalizeLoudness():
    return 0

def normalizeLiveness():
    return 0

def normalizeValence():
    return 0