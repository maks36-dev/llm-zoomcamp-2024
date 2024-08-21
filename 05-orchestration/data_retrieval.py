from typing import Dict, List
from elasticsearch import Elasticsearch


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')

    script_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": "When is the next cohort?",
                        "fields": ["question^4", "text^2", "section"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    es_client = Elasticsearch(connection_string)
    
    try:
        response = es_client.search(
            index=index_name,
            body= script_query,   
        )
        return [hit['_source'] for hit in response['hits']['hits']]
    except Exception as e:
        print(e)
        return []