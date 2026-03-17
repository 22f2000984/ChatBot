# from scraper import scrape
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS

# urls = [
#     "https://www.starsolutions.com/products/",
#     "https://www.starsolutions.com/industry-4-0/?doing_wp_cron=1773721292.0095050334930419921875"
# ]

# docs = [scrape(u) for u in urls]

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=50
# )

# chunks = []
# for d in docs:
#     chunks.extend(splitter.split_text(d))

# embeddings = OpenAIEmbeddings()

# db = FAISS.from_texts(chunks, embeddings)
# db.save_local("vectorstore")

# print("✅ Vector DB created")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

BASE_URL = "https://www.starsolutions.com"

visited = set()
to_visit = [BASE_URL]

all_text = []

# ── SCRAPE FUNCTION ─────────────────────────────
def scrape(url):
    try:
        print(f"Scraping: {url}")
        r = requests.get(url, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        # Remove scripts/styles
        for s in soup(["script", "style", "nav", "footer"]):
            s.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text, soup

    except Exception as e:
        print("Error:", url, e)
        return "", None


# ── LINK FILTER ────────────────────────────────
def get_links(soup, base_url):
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        full_url = urljoin(base_url, href)

        # keep only same domain
        if urlparse(full_url).netloc == urlparse(BASE_URL).netloc:
            links.append(full_url)

    return links


# ── CRAWLER ────────────────────────────────────
while to_visit:

    url = to_visit.pop(0)

    if url in visited:
        continue

    visited.add(url)

    text, soup = scrape(url)

    if text:
        all_text.append(text)

    if soup:
        new_links = get_links(soup, url)

        for link in new_links:
            if link not in visited:
                to_visit.append(link)

    # limit crawl (IMPORTANT)
    if len(visited) > 50:
        break


print(f"\nTotal pages scraped: {len(visited)}")

# ── CHUNKING ───────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = []

for doc in all_text:
    chunks.extend(splitter.split_text(doc))


# ── EMBEDDINGS ─────────────────────────────────
embeddings = OpenAIEmbeddings()

db = FAISS.from_texts(chunks, embeddings)

db.save_local("vectorstore")

print("✅ Full website vector DB created")