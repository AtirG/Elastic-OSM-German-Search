from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://localhost:9200",
    request_timeout=30,
)