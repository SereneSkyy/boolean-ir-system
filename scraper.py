import requests
from bs4 import BeautifulSoup
import os
import time

# Wikipedia article titles (use exact title as it appears in the URL)
TOPICS = [
    "Information_retrieval",
    "Boolean_model_of_information_retrieval",
    "Inverted_index",
    "Search_engine",
    "Web_crawler",
    "Natural_language_processing",
    "Text_mining",
    "Relevance_(information_retrieval)"
]

BASE_URL = "https://en.wikipedia.org/wiki/"
OUTPUT_DIR = "docs"
HEADERS = {"User-Agent": "TECH400/1.0 (educational use)"}

def scrape_article(topic):
    url = BASE_URL + topic
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Wikipedia article body lives inside <div id="mw-content-text">
    content_div = soup.find("div", {"id": "mw-content-text"})
    paragraphs = content_div.find_all("p")

    # Join paragraph text, skip empty ones
    text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())

    return text

def save_document(topic, text):
    filename = topic.replace("_", "-").lower() + ".txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved: {filepath} ({len(text)} characters)")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for topic in TOPICS:
        try:
            text = scrape_article(topic)
            save_document(topic, text)
            time.sleep(1)  # be polite — don't hammer the server with rapid requests
        except Exception as e:
            print(f"Failed to scrape {topic}: {e}")

if __name__ == "__main__":
    main()