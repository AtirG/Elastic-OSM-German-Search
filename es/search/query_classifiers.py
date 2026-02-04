import re

def is_likely_house_number(token: str) -> bool:
    token = token.lower()
    return bool(re.fullmatch(r"\d{1,4}[a-z]?", token))

def is_likely_postcode(token: str) -> bool:
    return token.isdigit() and len(token) == 5

def decompound_suffixes(text: str) -> str:
    """
    Split compound German street names into component parts.
    Example: "ringbahnstrasse" -> "ringbahn strasse"
    """
    street_suffixes = r"(strasse|straße|gasse|allee|alle|weg|ufer|damm|stieg|platz)"
    # The regex uses \b (word boundary) to ensure we match complete words
    # This will split things like "Ringbahnstrasse" -> "Ringbahn strasse"
    return re.sub(rf"(\w+)({street_suffixes})\b", r"\1 \2", text, flags=re.IGNORECASE)

def classify_query(q):
    q = q.strip()
    tokens = q.split()
    housenumber = None
    postcode = None

    for token in tokens:
        if len(tokens) >= 2 and not housenumber and is_likely_house_number(token):
            housenumber = token
        elif not postcode and is_likely_postcode(token):
            postcode = token

    # decompound suffixes only in full query text, not individual tokens
    decompounded_query = decompound_suffixes(q)

    return {
        "full_query": decompounded_query,
        "housenumber": housenumber,
        "postcode": postcode
    }


# this uses the function classify_query to determine if the query is
def process_classification(q: str):
    """
    Wrapper for the classify_query logic used in the route.

    """
    classification = classify_query(q)

    q = classification["full_query"]
    housenumber = classification["housenumber"]
    postcode = classification["postcode"]

    # keep your prints exactly the same
    print(
        f"housenumber: {housenumber}\n"
        f"postcode = {postcode}\n"
        f"query: {q}"
    )

    return q, housenumber, postcode







