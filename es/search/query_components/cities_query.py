def get_city_matches(q, housenumber=None, postcode=None):
    if housenumber or postcode:
        return []  # Skip city matches if we have a full addresses

    return [
        # boost on type
        {
            "bool": {
                "must": [
                    {"term": {"is_city": "1"}},
                    {"match_phrase": {"city": {"query": q}}}
                ],
                "must_not": [
                    {"term": {"is_street": "1"}}
                ],
                "boost": 20
            }
        },

        # boost for type = city
        {
            "bool": {
                "must": [
                    {"term": {"is_city": "1"}},
                    {"term": {"place": "city"}},
                    {"match": {"city": {"query": q, "operator": "and"}}}
                ],
                "boost": 10
            }
        },

        # broader match on city name
        {
            "bool": {
                "must": [
                    {"term": {"is_city": "1"}},
                    {"match_phrase": {"city": {"query": q}}}
                ],
                "must_not": [
                    {"term": {"is_street": "1"}}
                ],
                 "boost": 1000
            }
        },
    ]