from elasticsearch import Elasticsearch, helpers

elastic_pwd_file = open('docker_elastic_pwd.txt', 'r')
elastic_pwd = elastic_pwd_file.read()
elastic_pwd_file.close()

es = Elasticsearch('https://localhost:9200', ca_certs="http_ca.crt", basic_auth=("elastic", elastic_pwd))

response = es.indices.delete(index='songs')
print(response)
print(es.indices.exists(index='songs'))