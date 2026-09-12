# Boolean Information Retrieval System
**TECH 400 — Week 2 Assignment**

A simple Boolean Information Retrieval (IR) system built from scratch in Python.
The system scrapes a small document collection from Wikipedia, preprocesses the
text, builds a dictionary and inverted index, and supports Boolean (AND / OR / NOT)
queries over the collection.

## Project Structure

```
boolean-ir-system/
├── docs/                   # 8 scraped documents (corpus)
├── screenshots/            # Screenshots for this report
├── scraper.py              # Scrapes documents from Wikipedia
├── preprocess.py           # Tokenization, stopword removal, stemming
├── indexer.py              # Builds dictionary + inverted index
├── boolean_search.py       # AND / OR / NOT query logic
├── main.py                 # Interactive CLI entry point
├── inverted_index.json     # Generated inverted index (term -> doc IDs)
├── doc_map.json            # Generated doc ID -> filename map
└── requirements.txt               # dependencies           
└── README.md                # This report
```

## 1. Document Collection

Instead of using a toy dataset, I built a small web scraper (`scraper.py`) using
`requests` and `BeautifulSoup` to pull real content directly from Wikipedia. This
let me practice a practical, in-demand skill (web scraping) while producing a
document collection relevant to the course itself.

**Topics scraped** (8 documents, satisfying the assignment's 5–10 document requirement):
- Information retrieval
- Boolean model of information retrieval
- Inverted index
- Search engine
- Web crawler
- Natural language processing
- Text mining
- Relevance (information retrieval)

**Design choices:**
- A custom `User-Agent` header was set to identify the scraper transparently,
  following good scraping etiquette rather than disguising the traffic as a browser.
- A 1-second delay (`time.sleep(1)`) was added between requests to avoid
  overloading Wikipedia's servers — basic rate-limiting/politeness practice.
- Only the main article text (`<p>` tags inside `mw-content-text`) was extracted,
  filtering out navigation, references, and infobox clutter.

## 2. Text Preprocessing

Raw scraped text is noisy and inconsistent, so `preprocess.py` implements a
standard IR preprocessing pipeline:

1. **Lowercasing** — ensures "Boolean" and "boolean" are treated as the same term.
2. **Cleaning** — regex removes punctuation, digits, and symbols, keeping only letters.
3. **Tokenization** (NLTK `word_tokenize`) — splits text into individual word tokens.
4. **Stopword removal** (NLTK's English stopword list) — removes common low-information
   words like "the", "is", "and" that would otherwise bloat the index without helping
   distinguish documents.
5. **Stemming** (Porter Stemmer) — reduces words to a common root (e.g. "retrieval",
   "retrieving", "retrieves" → `retriev`) so that different grammatical forms of the
   same concept are indexed as one term.

The same preprocessing pipeline is applied both when building the index and when
parsing a user's search query, which is essential — otherwise a query for "Retrieval"
would fail to match the indexed term `retriev`.

## 3. Dictionary & Inverted Index

`indexer.py` reads all documents in `docs/`, preprocesses each one, and builds:

- **Dictionary** — the set of all unique terms across the entire collection.
- **Inverted index** — a mapping of `term → [list of document IDs containing that term]`.

Because this assignment implements the classic **Boolean retrieval model**
(Manning et al., Ch. 1), each posting records only whether a term is *present* in a
document — not how many times it occurs. Term frequency is used in ranked/vector
space retrieval models, which is outside this assignment's scope.

**Collection statistics:**
- Total documents indexed: **[YOUR NUMBER]**
- Total unique terms (dictionary size): **[YOUR NUMBER]**

Both `inverted_index.json` and `doc_map.json` are saved to disk so the index can be
reloaded without rebuilding it every time.

## 4. Boolean Search Implementation

`boolean_search.py` implements the three core Boolean operators using Python
`set` operations over the postings lists:

| Operator | Implementation | Meaning |
|---|---|---|
| AND | `set1 & set2` | Documents containing **both** terms |
| OR  | `set1 \| set2` | Documents containing **either** term |
| NOT | `all_docs - set` | Documents **not** containing the term |

Supported query formats: `term`, `term1 AND term2`, `term1 OR term2`, `NOT term`.

**Sample queries and results:**

| Query | Result |
|---|---|
| `boolean` | [X documents — list them] |
| `search AND engine` | [X documents] |
| `crawler OR index` | [X documents] |
| `NOT boolean` | [X documents] |


## 5. Interactive CLI

`main.py` provides a menu-driven interface to build the index, browse the
dictionary, and run Boolean queries interactively — without needing to touch code.

## 6. How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/boolean-ir-system.git
cd boolean-ir-system

# 2. Set up virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows
source venv/bin/activate       # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Scrape documents (already included in docs/, but can be re-run)
python scraper.py

# 5. Run the system
python main.py
```

