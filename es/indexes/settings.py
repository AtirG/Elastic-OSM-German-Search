SETTINGS = {
    "number_of_shards": 5,
    "analysis": {
        "filter": {
            "street_suffix_capture": {
                "type": "pattern_capture",
                "preserve_original": False,
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
            "german_normalization": {
                "type": "german_normalization"
            }
        },
        "char_filter": {
            "street_suffix_splitter": {
                "type": "pattern_replace",
                "pattern": "(.+?)(strasse|straße|gasse|allee|alle|weg|ufer|damm|stieg|platz)$",
                "replacement": "$1 $2"
            },
            "housenumber_char_filter": {
                "type": "pattern_replace",
                "pattern": "([0-9])([a-zA-Z])",
                "replacement": "$1 $2"
            }
        },
        "analyzer": {
            "address_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "char_filter": ["street_suffix_splitter"],
                "filter": [
                    "lowercase",
                    "german_normalization",
                    "street_suffix_capture",
                    "unique",
                    "autocomplete_edge_light"
                ]
            },
            "address_search": {
                "type": "custom",
                "tokenizer": "standard",
                "char_filter": ["street_suffix_splitter"],
                "filter": [
                    "lowercase",
                    "german_normalization",
                    "street_suffix_capture",
                    "unique"
                ]
            }
        }
    }
}