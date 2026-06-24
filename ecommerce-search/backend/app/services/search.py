# app/services/search.py
from elasticsearch import Elasticsearch
from app.config import settings

# Initialize the ES client using config values
es_client = Elasticsearch(
    f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"
)

INDEX_NAME = "products"

def create_product_index():
    """Creates the products index with custom mappings for full-text and autocomplete."""
    if es_client.indices.exists(index=INDEX_NAME):
        return

    settings_mappings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "search_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "snowball"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "category_id": {"type": "integer"},
                "name": {
                    "type": "text", 
                    "analyzer": "search_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "description": {"type": "text", "analyzer": "search_analyzer"},
                "price": {"type": "float"},
                "rating": {"type": "float"},
                "in_stock": {"type": "boolean"}
            }
        }
    }
    
    es_client.indices.create(index=INDEX_NAME, **settings_mappings)

def index_product(product):
    """Indexes or updates a single product document in ES."""
    doc = {
        "id": product.id,
        "category_id": product.category_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "rating": product.rating,
        "in_stock": product.in_stock
    }
    es_client.index(index=INDEX_NAME, id=str(product.id), document=doc)

def search_products_in_es(query: str, category_id: int | None = None, min_price: float | None = None, max_price: float | None = None):
    """Executes a fuzzy full-text search against Elasticsearch with boolean filters."""
    
    # Base search body with multi-match full-text capabilities
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["name^2", "description"],  # Boosting name matches over description
                            "fuzziness": "AUTO"                   # Typo tolerance
                        }
                    }
                ],
                "filter": []
            }
        }
    }
    
    # Append precise structural filters if provided
    if category_id:
        search_body["query"]["bool"]["filter"].append({"term": {"category_id": category_id}})
        
    if min_price is not None or max_price is not None:
        price_range = {}
        if min_price is not None:
            price_range["gte"] = min_price
        if max_price is not None:
            price_range["lte"] = max_price
        search_body["query"]["bool"]["filter"].append({"range": {"price": price_range}})

    response = es_client.search(index=INDEX_NAME, **search_body)
    
    # Extract structural source documents from ES hits
    hits = response["hits"]["hits"]
    return [hit["_source"] for hit in hits]