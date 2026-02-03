def get_germany_template():
    """
    Returns the configuration for German address logic.
    Targeted at indices starting with 'osm_de_'
    """
    return {
        "index_patterns": ["osm_de_*"],
        "template": {
            "settings": {
                "number_of_shards": 5,
                "analysis": {
                    "filter": {
                        "street_suffix_capture": {
                            "type": "pattern_capture",
                            "preserve_original": "false",
                            "patterns": [
                                "(.+?)(strasse|straße|gasse|allee|alle|weg|ufer|damm|stieg|platz)$",
                                "(strasse|straße|gasse|allee|alle|weg|ufer|damm|stieg|platz)$"
                            ]
                        },
                        "autocomplete_edge_light": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 15
                        },
                        "german_normalization": { "type": "german_normalization" }
                    },
                    "char_filter": {
                        "street_suffix_splitter": {
                            "pattern": "(.+?)(strasse|straße|gasse|allee|alle|weg|ufer|damm|stieg|platz)$",
                            "type": "pattern_replace",
                            "replacement": "$1 $2"
                        },
                        "housenumber_char_filter": {
                            "pattern": "([0-9])([a-zA-Z])",
                            "type": "pattern_replace",
                            "replacement": "$1 $2"
                        }
                    },
                    "analyzer": {
                        "address_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "char_filter": ["street_suffix_splitter"],
                            "filter": ["lowercase", "german_normalization", "street_suffix_capture", "unique", "autocomplete_edge_light"]
                        },
                        "address_search": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "char_filter": ["street_suffix_splitter"],
                            "filter": ["lowercase", "german_normalization", "street_suffix_capture", "unique"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "uid": { "type": "keyword" },
                    "name": { "type": "text", "analyzer": "address_analyzer", "search_analyzer": "address_search" },
                    "street": { "type": "text", "analyzer": "address_analyzer", "search_analyzer": "address_search" },
                    "housenumber": {
                        "type": "keyword",
                        "fields": { "text": { "type": "text", "analyzer": "standard" } }
                    },
                    "postcode": { "type": "keyword" },
                    "city": { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
                    "lat": { "type": "double" },
                    "lon": { "type": "double" },
                    "country_code": { "type": "keyword" },
                    "display_address": { "type": "text", "index": False }
                }
            }
        },
        "priority": 100
    }