from upstash_redis import Redis
import re
from pymongo import MongoClient
from collections import Counter
from nltk.corpus import stopwords
import nltk
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import math
from flask import Flask, request, jsonify

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

app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    print(q)
    if not q:
        return jsonify({
            "error": "Query parameter 'q' is required"
        })
    
    query_tokens = preprocess(q)
    print(query_tokens)

    if not query_tokens:
        return jsonify({
            "results": []
        })
    
    total_docs = int(redis.get("stats:total_docs") or 0)

    doc_scores = {}

    for token in query_tokens:
        indexed_docs = redis.hgetall(f"term:{token}")

        if not indexed_docs:
            continue

        df = int(redis.get(f"df:{token}") or 0)

        # calculate idf

        idf = math.log(total_docs / df)

        # calculate scores for each doc containing the term

        for doc_id, tf in indexed_docs.items():
            tf = float(tf)
            doc_len = int(redis.hget(f"doc_clen:{doc_id}", "clen") or 0)
            normalized_tf = tf / doc_len if doc_len > 0 else 0

            doc_scores[doc_id] = normalized_tf * idf

        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []

        for doc_id, score in ranked_docs[:10]:
            doc = docs.find_one({
                "_id": ObjectId(str(doc_id))
            })

            if doc:
                results.append({
                    "title": doc.get("title", ""),
                    "url": doc.get("url", ""),
                    "summary": doc.get("clean_text", "")[:200] + "...",
                    "score": score
                })
        print(results)

        return jsonify({
            "results": results
        })
    
if __name__ == "__main__":
    app.run(debug=True)