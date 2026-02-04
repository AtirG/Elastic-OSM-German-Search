from es.search.query_components.addresses_query import get_full_address_matches
from es.search.query_components.cities_query import get_city_matches
from es.search.query_components.city_boosts import get_city_boost_function
from es.search.query_components.streets_query import get_street_matches


def build_address_search_body(q, housenumber, postcode):
    """
    Builds the exact same Elasticsearch query body used in the route.
    No logic changed.
    """
    body = {
        "size": 3,
        "explain": True,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "should": [
                            *get_city_matches(q, housenumber, postcode),
                            *get_street_matches(q, postcode, housenumber),
                            *get_full_address_matches(q, housenumber, postcode),
                        ],
                        "minimum_should_match": 1
                    }
                },
                "functions": [
                    get_city_boost_function(q),
                ],
                "boost_mode": "sum"
            }
        },
        "collapse": {
            "field": "city.keyword",
            "inner_hits": {
                "name": "street_group",
                "collapse": {
                    "field": "postcode"  # NO .keyword needed here
                },
                "size": 1
            }
        }
    }

    return body