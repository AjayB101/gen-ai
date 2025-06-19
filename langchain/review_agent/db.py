import pandas as pd
import uuid
import chromadb
from chromadb import PersistentClient

client = PersistentClient("my_chroma_db")
collection = client.get_or_create_collection("my_collection")


def setup_chroma_if_needed():
    df = pd.read_csv("realistic_restaurant_reviews.csv")
    if not collection.count():
        for _, row in df.iterrows():
            collection.add(
                # ✅ wrap in list
                documents=[f"{row['Title']} {row['Review']}"],
                metadatas=[{"rating": row["Rating"], "date": row["Date"]}],
                ids=[str(uuid.uuid4())],
            )


def get_review(query: list[str], n_results=2):

    collection = collection = client.get_or_create_collection("my_collection")
 # however you're getting your collection
    results = collection.query(query_texts=query, n_results=n_results)
    print("Result =========", results)
    return results
