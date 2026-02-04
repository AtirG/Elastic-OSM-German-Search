def get_full_address_matches(q, housenumber=None, postcode=None):
    if not housenumber:
        return []

    queries = []

    if not postcode:
        queries.append({
            "bool": {
                "must": [
                    {
                        "match": {
                            "merged_address": {
                                "query": q,
                                "operator": "or",
                                "minimum_should_match": "90%"
                            }
                        }
                    },
                    {
                        "match": {
                            "housenumber.text": {
                                "query": housenumber,
                                "operator": "and"
                            }
                        }
                    }
                ],
                "should": [
                    {"term": {"is_full_address": 1}}
                ],
                "boost": 400
            }
        })

    elif postcode and housenumber:
        street_tokens = [
            tok for tok in q.split()
            if tok.lower() not in {postcode.lower(), housenumber.lower()}
               and not tok.isdigit()
        ]

        street_query = " ".join(street_tokens)

        queries.append({
            "bool": {
                "must": [
                    {
                        "match": {
                            "merged_address": {
                                "query": street_query,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match": {
                            "housenumber.text": {
                                "query": housenumber,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "term": {
                            "postcode": postcode
                        }
                    }
                ],
                "should": [
                    {"term": {"is_full_address": {"value": 1, "boost": 50}}},
                    {"match": {"housenumber.text": {"query": housenumber, "operator": "and", "boost": 20}}},
                    {"term": {"postcode": {"value": postcode, "boost": 20}}}
                ],
                "boost": 100
            }
        })

    return queries
