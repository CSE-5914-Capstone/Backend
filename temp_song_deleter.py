from elasticsearch import Elasticsearch, helpers

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

if(not es.indices.exists(index='songs')):
    print("No songs index: ready to index with song_query")
else:
    print("Clearing song index")    
    response = es.indices.delete(index='songs')
    print(response)
    print(es.indices.exists(index='songs'))
    print("No songs index: ready to index with song_query")