
from es.client import es1 as es
from es.search.helper_funcions import  normalize_and_validate_query
from es.search.query_classifiers import process_classification
from es.search.query_body import build_address_search_body
from es.search.query_results import parse_es_hits


def search_addresses(raw_q: str):
    """
    Full wrapper for the address search flow.
    Keeps logic EXACTLY the same as in the original route.
    """

    # 1. normalize and validate
    q = normalize_and_validate_query(raw_q)
    if q is None:
        return []   # route will wrap jsonify()

    # 2. classify
    q, housenumber, postcode = process_classification(q)

    # 3. build ES body
    body = build_address_search_body(q, housenumber, postcode)

    # 4. execute the search
    resp = es.search(index="osm_addresses_de_v1", body=body)
    hits = resp.get("hits", {}).get("hits", [])

    # 5. parse results (prints + description logic)
    results = parse_es_hits(hits)

    return results