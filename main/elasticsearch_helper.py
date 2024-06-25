from elasticsearch import Elasticsearch

# Configuration de la connexion à Elasticsearch
es = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]
)

def create_index(index_name):
    # Création d'un index dans Elasticsearch
    es.indices.create(index=index_name, ignore=400)

def index_document(index_name, doc_type, document):
    # Indexation d'un document dans Elasticsearch
    es.index(index=index_name, doc_type=doc_type, body=document)

def search_document(index_name, query):
    # Recherche d'un document dans Elasticsearch
    return es.search(index=index_name, body=query)

