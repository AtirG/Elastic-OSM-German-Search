def normalize_and_validate_query(raw_q: str) -> str | None:
    """
    Normalize the query string and enforce minimal constraints.

    Returns:
        - normalized query (str) if valid
        - None if query is too short / invalid
    """
    q = (raw_q or "").strip().lower()

    # reject if less than 2 chars *and* not purely digits
    if len(q) < 2 and not q.isdigit():
        return None

    return q


# printing the explanation in the backend for the results. by scores and shows the resutls
def print_explanation(hit):
    explanation = hit.get("_explanation", {})

    print("ID:", hit["_id"])
    print("Score:", hit.get("_score"))
    print("Matched Fields:")

    def extract_matches(exp, level=0):
        if "description" in exp:
            indent = "  " * level
            print(f"{indent}- {exp['description']} : {exp.get('value', '')}")
            for detail in exp.get("details", []):
                extract_matches(detail, level + 1)

    extract_matches(explanation)
    print("=" * 30)



