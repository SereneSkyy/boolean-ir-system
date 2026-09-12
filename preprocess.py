import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

STOP_WORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()


def clean_text(text):
    """Lowercase and strip out non-alphabetic characters (keep spaces)."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)  # remove numbers, punctuation, symbols
    return text


def tokenize(text):
    """Split cleaned text into word tokens."""
    return word_tokenize(text)


def remove_stopwords(tokens):
    """Filter out common stopwords and very short tokens."""
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def stem_tokens(tokens):
    """Reduce words to their root form (e.g., 'retrieving' -> 'retriev')."""
    return [STEMMER.stem(t) for t in tokens]


def preprocess(text):
    """
    Full pipeline: clean -> tokenize -> remove stopwords -> stem.
    Returns a list of processed term tokens.
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = stem_tokens(tokens)
    return tokens


if __name__ == "__main__":
    # Quick manual test
    sample = "Information Retrieval systems help users find relevant documents efficiently!"
    print("Original:", sample)
    print("Processed:", preprocess(sample))