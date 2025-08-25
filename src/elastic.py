from elasticsearch import Elasticsearch
import os

def get_es_client():
    es_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")  # Default to localhost if not set
    return Elasticsearch(es_url)

es_client = get_es_client()

mappings = {
    "mappings": {
        "properties": {
            "lodgde": {"type": "text"},
            "labelguidanceelement": {"type": "text"},
            "descguidanceelement": {"type": "text"},
            "bodyguidanceelement": {"type": "text"},
            "actor": {"type": "keyword"},
            "criterion": {"type": "keyword"},
            "domain": {"type": "keyword"},
            "focus": {"type": "keyword"},
            "motivation": {"type": "keyword"},
            "test": {"type": "keyword"},
            "type": {"type": "keyword"},
            "source": {"type": "keyword"}
        }
    }
}
