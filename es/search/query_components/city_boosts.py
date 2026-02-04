def get_city_boost_function(q):
    return {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"is_city": "1"}},
                    {"match": {"merged_address": {"query": q}}}
                ]
            }
        },
        "weight": 1500
    }
