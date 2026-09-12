from preprocess import preprocess
from indexer import load_index

ALL_DOC_IDS = None  # will be set once doc_map is loaded


def get_postings(term, inverted_index):
    """
    Returns the postings list (sorted list of doc_ids) for a single term,
    after applying the same preprocessing (stemming etc.) used at index time.
    """
    processed = preprocess(term)
    if not processed:
        return []
    stemmed_term = processed[0]  # single-word term assumed
    return set(inverted_index.get(stemmed_term, []))


def boolean_and(list1, list2):
    return list1 & list2  # set intersection


def boolean_or(list1, list2):
    return list1 | list2  # set union


def boolean_not(term_set, all_docs):
    return all_docs - term_set  # set difference


def process_query(query, inverted_index, all_doc_ids):
    """
    Supports simple two-operand queries in the form:
        "term1 AND term2"
        "term1 OR term2"
        "NOT term1"
    Operators must be UPPERCASE. Case-insensitive terms are handled by preprocess().
    """
    tokens = query.strip().split()

    # Case: NOT term
    if tokens[0].upper() == "NOT" and len(tokens) == 2:
        term_set = get_postings(tokens[1], inverted_index)
        result = boolean_not(term_set, all_doc_ids)
        return result

    # Case: term1 AND/OR term2
    if len(tokens) == 3 and tokens[1].upper() in ("AND", "OR"):
        term1, operator, term2 = tokens
        set1 = get_postings(term1, inverted_index)
        set2 = get_postings(term2, inverted_index)

        if operator.upper() == "AND":
            return boolean_and(set1, set2)
        elif operator.upper() == "OR":
            return boolean_or(set1, set2)

    # Case: single term, no operator
    if len(tokens) == 1:
        return get_postings(tokens[0], inverted_index)

    raise ValueError(
        "Unsupported query format. Use: 'term', 'term1 AND term2', "
        "'term1 OR term2', or 'NOT term'."
    )


def run_query(query, inverted_index, doc_map):
    all_doc_ids = set(int(k) for k in doc_map.keys())
    result_ids = process_query(query, inverted_index, all_doc_ids)
    result_docs = [doc_map[str(doc_id)] for doc_id in sorted(result_ids)]
    return result_docs


if __name__ == "__main__":
    inverted_index, doc_map = load_index()

    test_queries = [
        "boolean",
        "boolean AND retrieval",
        "search OR crawler",
        "NOT crawler",
    ]

    for q in test_queries:
        results = run_query(q, inverted_index, doc_map)
        print(f"\nQuery: '{q}'")
        print(f"Matching documents ({len(results)}):")
        for doc in results:
            print(f"  - {doc}")