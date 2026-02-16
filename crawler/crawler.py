import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag, urlunparse
from collections import deque
import time
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import re
import datetime

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
docs = db["docs"]

SEED_URLS = [
    "https://en.wikipedia.org/wiki/Computer_science",
    "https://en.wikipedia.org/wiki/Artificial_intelligence"
]

MAX_PAGES = 50
MAX_DEPTH = 2
DELAY = 2

visited = set()
queue = deque()

for url in SEED_URLS:
    queue.append((url, 0))

def is_valid_wiki_url(url):
    parsed = urlparse(url)

    # Must be Wikipedia domain
    if parsed.netloc != "en.wikipedia.org":
        return False

    # Must start with /wiki/
    if not parsed.path.startswith("/wiki/"):
        return False

    # Avoid special pages
    if ":" in parsed.path:
        return False
    
    # Avoid # links
    if "#" in parsed.path:
        return False

    return True

def normalize_url(url):
    url, _ = urldefrag(url)  # remove fragment
    
    parsed = urlparse(url)
    
    # Remove query parameters
    cleaned = parsed._replace(query="")
    
    return urlunparse(cleaned)

def extract_clean_text(soup):
    # Remove unwanted sections
    for tag in soup(['script', 'style', 'sup', 'table']):
        tag.decompose()

    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div:
        return ""

    paragraphs = content_div.find_all("p")
    text = " ".join(p.get_text() for p in paragraphs)

    # Basic cleaning
    text = re.sub(r'\[\d+\]', '', text)  # remove citation numbers [1]
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def crawl():
    pages_crawled = 0

    while queue and pages_crawled < MAX_PAGES:
        url, depth = queue.popleft()

        if url in visited or depth > MAX_DEPTH:
            continue

        try:
            print(f"Crawling: {url} (Depth: {depth})")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"
            }

            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code != 200:
                print(f"Failed to retrieve {url} (Status code: {response.status_code})")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title_tag = soup.find('title')
            title = title_tag.get_text() if title_tag else ""
            clean_text = extract_clean_text(soup)

            outlinks = []

            for link in soup.find_all('a', href=True):
                abs_url = urljoin(url, link['href'])
                abs_url = normalize_url(abs_url)

                if is_valid_wiki_url(abs_url) and abs_url:
                    outlinks.append(abs_url)

                    if abs_url not in visited:
                        queue.append((abs_url, depth + 1))
            
            new_doc = {
                "url": url,
                "title": title,
                "clean_text": clean_text,
                "outlinks": outlinks,
                "created_at": datetime.datetime.now()
            }
            
            docs.insert_one(new_doc)

            print("Doc added!")

            visited.add(url)
            pages_crawled += 1

            time.sleep(DELAY)
        
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            continue