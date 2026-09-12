import os
import json
from preprocess import preprocess

DOCS_DIR = "docs"
INDEX_FILE = "inverted_index.json"
DOC_MAP_FILE = "doc_map.json"


def load_documents(docs_dir=DOCS_DIR):
    """
    Reads all .txt files from docs_dir.
    Returns a dict: {doc_id: filename}, and {doc_id: raw_text}
    """
    doc_map = {}
    doc_texts = {}
    filenames = sorted(f for f in os.listdir(docs_dir) if f.endswith(".txt"))

    for doc_id, filename in enumerate(filenames, start=1):
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        doc_map[doc_id] = filename
        doc_texts[doc_id] = text

    return doc_map, doc_texts


def build_inverted_index(doc_texts):
    """
    Builds an inverted index: {term: [doc_id1, doc_id2, ...]}
    Also builds a dictionary: sorted list of all unique terms.
    """
    inverted_index = {}

    for doc_id, text in doc_texts.items():
        terms = preprocess(text)
        unique_terms = set(terms)  # doc-level presence, not term frequency (Boolean model)

        for term in unique_terms:
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append(doc_id)

    # Sort postings lists for consistency
    for term in inverted_index:
        inverted_index[term] = sorted(inverted_index[term])

    return inverted_index


def save_index(inverted_index, doc_map):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, indent=2)
    with open(DOC_MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(doc_map, f, indent=2)
    print(f"Saved inverted index -> {INDEX_FILE}")
    print(f"Saved document map -> {DOC_MAP_FILE}")


def load_index():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        inverted_index = json.load(f)
    with open(DOC_MAP_FILE, "r", encoding="utf-8") as f:
        doc_map = json.load(f)
    return inverted_index, doc_map


def build_and_save():
    doc_map, doc_texts = load_documents()
    inverted_index = build_inverted_index(doc_texts)
    save_index(inverted_index, doc_map)

    # Print summary stats — useful for the report
    print(f"\nTotal documents indexed: {len(doc_map)}")
    print(f"Total unique terms (dictionary size): {len(inverted_index)}")
    return inverted_index, doc_map


if __name__ == "__main__":
    build_and_save()