from upstash_redis import Redis
import re
from pymongo import MongoClient
from collections import Counter
from nltk.corpus import stopwords
import nltk
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

nltk.download('stopwords')

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
docs = db["docs"]

redis = Redis.from_env()

stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)

    tokens = []

    for word in words:
        if word not in stop_words:
            tokens.append(word)

    return tokens

def index_doc(doc):
    doc_id = str(doc["_id"])
    text = doc.get("clean_text", "")

    tokens = preprocess(text)

    if not tokens:
        return
    
    term_counts = Counter(tokens)
    content_length = len(tokens)

    redis.hset(f"doc_clen:{doc_id}", "clen", str(content_length))

    for term, tf in term_counts.items():
        redis.hset(f"term:{term}", doc_id, tf)
        redis.incr(f"df:{term}")
        print(f"Indexed term '{term}' for doc {doc_id} with tf={tf}")

    redis.incr("stats:total_docs")
    print(f"Indexed doc {doc_id} - {doc.get('title', '')}")

if __name__ == "__main__":
    while True:
        doc_id = redis.rpop("wikidocs_queue")
        if doc_id is None:
            continue
        
        doc = docs.find_one({
            "_id": ObjectId(str(doc_id))
        })
        if doc:
            index_doc(doc)
