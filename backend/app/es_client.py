# es_client.py
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_USER = os.getenv("ES_USER", None)
ES_PASS = os.getenv("ES_PASS", None)

def get_es_client():
    if ES_USER and ES_PASS:
        return Elasticsearch(ES_HOST, basic_auth=(ES_USER, ES_PASS))
    return Elasticsearch(ES_HOST)
