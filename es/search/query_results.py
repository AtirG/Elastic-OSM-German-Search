from es.search.helper_funcions import print_explanation


def build_result_item(hit):
    source = hit["_source"]

    name = (source.get("name") or "").strip()
    display_address = source.get("display_address", "")
    place = source.get("place", "")
    is_city = source.get("is_city", "0")

    # identical logic
    if is_city == "1" and place:
        description = f"{display_address}, {place}"
    elif name:
        description = f"{name} {display_address}"
    else:
        description = display_address

    return {
        "description": description,
        **source
    }


#uses both print explanation of the results and built the result for the frontend
def parse_es_hits(hits):
    results = []

    for hit in hits:
        # keep prints
        #print_explanation(hit)

        item = build_result_item(hit)
        results.append(item)

    return results


