from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://elasticsearch:9200",
    request_timeout=30,
)


es1 = Elasticsearch(
    "http://localhost:9200",
    request_timeout=30,
)