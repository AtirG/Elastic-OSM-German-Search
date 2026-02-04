MAPPINGS = {
    "_routing": {"required": True},
    "properties": {
        "uid": {"type": "keyword"},

        "name": {"type": "text"},
        "street": {
            "type": "text",
            "analyzer": "address_analyzer",
            "search_analyzer": "address_search"
        },
        "housenumber": {
            "type": "keyword",
            "fields": {
                "text": {
                    "type": "text",
                    "analyzer": "address_analyzer"
                }
            }
        },
        "postcode": {"type": "keyword"},
        "city_name": {
            "type": "text",
            "fields": {"keyword": {"type": "keyword"}}
        },

        "lat": {"type": "double"},
        "lon": {"type": "double"},
        "location": {"type": "geo_point"},

        "is_city": {"type": "byte"},
        "is_street": {"type": "byte"},
        "is_place": {"type": "byte"},
        "is_full_address": {"type": "byte"},

        "country_code": {"type": "keyword"},
        "country_name": {"type": "keyword"},

        "display_address": {"type": "text", "index": False},

        "merged_address": {
            "type": "text",
            "analyzer": "address_analyzer",
            "search_analyzer": "address_search"
        }
    }
}