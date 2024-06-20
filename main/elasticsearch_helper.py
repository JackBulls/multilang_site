from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def create_index(index_name):
    es.indices.create(index=index_name, ignore=400)

def index_document(index_name, doc_type, document):
    es.index(index=index_name, doc_type=doc_type, body=document)

def search_document(index_name, query):
    return es.search(index=index_name, body=query)
