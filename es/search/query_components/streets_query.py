def get_street_matches(q, postcode=None, housenumber=None):
    # We’ll always produce the same two “strong” and “autocomplete” clauses,
    # but if postcode is set, we’ll boost those hits that carry the right PLZ.
    street_queries = []

    # 1) Strong, phrase‑match clause
    strong = {
        "bool": {
            "must": [
                {"term": {"is_street": "1"}},
                {"match_phrase": {"merged_address": {"query": q}}}
            ],
            # OPTIONAL: if you want to entirely *restrict* to that postcode,
            # swap this in for a must:
            # "must": [..., {"term": {"postcode": postcode}}]
            # but here we’ll leave it as a should‑boost so non‑matching PLZ still show up:
            **({"should": [
                {"term": {"postcode": {"value": postcode, "boost": 50}}}
            ]} if postcode else {}),
            "boost": 20
        }
    }
    street_queries.append(strong)

    # 2) Autocomplete‑style clause
    autocomplete = {
        "bool": {
            "must": [
                {"term": {"is_street": "1"}},
                {"match": {
                    "merged_address": {
                        "query": q,
                        "operator": "and"
                    }
                }}
            ],
            **({"should": [
                {"term": {"postcode": {"value": postcode, "boost": 100}}}
            ]} if postcode else {}),
            "boost": 300
        }
    }
    street_queries.append(autocomplete)

    return street_queries
