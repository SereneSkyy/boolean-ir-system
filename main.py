import os
from indexer import build_and_save, load_index, INDEX_FILE
from boolean_search import run_query


def index_exists():
    return os.path.exists(INDEX_FILE)


def build_index_menu():
    print("\nBuilding index from documents in 'docs/' ...")
    inverted_index, doc_map = build_and_save()
    return inverted_index, doc_map


def search_menu(inverted_index, doc_map):
    print("\n--- Boolean Search ---")
    print("Supported query formats:")
    print("  term")
    print("  term1 AND term2")
    print("  term1 OR term2")
    print("  NOT term")
    print("Type 'back' to return to main menu.\n")

    while True:
        query = input("Enter query: ").strip()
        if query.lower() == "back":
            break
        if not query:
            continue

        try:
            results = run_query(query, inverted_index, doc_map)
            print(f"\nQuery: '{query}'")
            if results:
                print(f"Found {len(results)} matching document(s):")
                for doc in results:
                    print(f"  - {doc}")
            else:
                print("No matching documents found.")
        except ValueError as e:
            print(f"Error: {e}")
        print()


def view_dictionary_menu(inverted_index):
    terms = sorted(inverted_index.keys())
    print(f"\nDictionary contains {len(terms)} unique terms.")
    print("First 30 terms (sample):")
    print(", ".join(terms[:30]))
    print()


def main():
    print("=" * 50)
    print(" Boolean Information Retrieval System")
    print("=" * 50)

    inverted_index, doc_map = None, None

    while True:
        print("\nMain Menu:")
        print("1. Build / Rebuild Index from documents")
        print("2. Search (Boolean queries)")
        print("3. View dictionary sample")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            inverted_index, doc_map = build_index_menu()

        elif choice == "2":
            if inverted_index is None:
                if index_exists():
                    inverted_index, doc_map = load_index()
                else:
                    print("\nNo index found. Please build the index first (option 1).")
                    continue
            search_menu(inverted_index, doc_map)

        elif choice == "3":
            if inverted_index is None:
                if index_exists():
                    inverted_index, doc_map = load_index()
                else:
                    print("\nNo index found. Please build the index first (option 1).")
                    continue
            view_dictionary_menu(inverted_index)

        elif choice == "4":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()