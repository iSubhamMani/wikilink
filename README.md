# 🧠 Distributed Search Engine (Wikipedia-Based)

A simple distributed search engine built using Python, Flask, MongoDB, and Redis.

This project crawls Wikipedia pages, indexes them using an inverted index, and provides a TF-IDF ranked search API.

---

## 📦 Project Structure

- **Crawler**
  - Crawls Wikipedia domain
  - Stores documents in MongoDB

- **Indexer**
  - Fetches documents from MongoDB
  - Preprocesses text:
    - Lowercasing
    - Tokenization
    - Stopword removal
  - Builds inverted index in Redis

- **API**
  - Flask-based search service
  - Implements TF-IDF ranking
  - Returns top ranked results
  - Fetches metadata from MongoDB

---

## 🧰 Tech Stack

- Python 3
- Flask
- MongoDB
- Redis
- NLTK
- BeautifulSoup
- Requests
