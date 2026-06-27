# src/router.py
from rank_bm25 import BM25Okapi

CLEARANCE_LEVELS = {
    "standard": 1,
    "top_secret": 2
}

def dual_engine_retrieve(query: str, clearance: str, corpus: list[dict], chroma_collection=None) -> list[dict]:
    """
    Acts as the Hybrid Search Router. It runs a semantic vector search (ChromaDB)
    and a keyword search (BM25), merging the results securely.
    """
    print(f"\n[ROUTER] Incoming Query: '{query}' | User Clearance: {clearance}")
    user_level = CLEARANCE_LEVELS.get(clearance, 0)

    hybrid_results = []

    # --- ENGINE 1: DENSE RETRIEVAL (ChromaDB) ---
    # TODO 1: Explain why we pass the security clearance directly into the ChromaDB 'where' filter
    # instead of filtering the documents manually in Python AFTER the database returns them.
    if chroma_collection is not None:
        dense_response = chroma_collection.query(
            query_texts=[query],
            n_results=5,
            where={"clearance_level": {"$lte": user_level}} # Database-level security filter
        )

        # Unpack the ChromaDB response into our standard dictionary format
        for i in range(len(dense_response["documents"][0])):
            hybrid_results.append({
                "text": dense_response["documents"][0][i],
                "clearance": dense_response["metadatas"][0][i].get("clearance", "standard"),
                "source": "dense_vector"
            })

    # --- ENGINE 2: SPARSE RETRIEVAL (BM25) ---
    safe_corpus = [
        doc for doc in corpus
        if CLEARANCE_LEVELS.get(doc.get("clearance", "standard"), 0) <= user_level
    ]

    if safe_corpus:
        tokenized_corpus = [doc["text"].lower().split(" ") for doc in safe_corpus]
        bm25_engine = BM25Okapi(tokenized_corpus)
        doc_scores = bm25_engine.get_scores(query.lower().split(" "))

        scored_docs = list(zip(safe_corpus, doc_scores))
        ranked_bm25 = [
            doc for doc, score in sorted(scored_docs, key=lambda x: x[1], reverse=True)
            if score > 0
        ]

        # Tag them so we know they came from the keyword search
        for doc in ranked_bm25:
            doc["source"] = "sparse_keyword"
            hybrid_results.append(doc)

    # --- THE MERGE (Deduplication) ---
    # TODO 2: What is the purpose of tracking 'seen_texts' using a Python Set,
    # and why do we only append documents if they are 'not in seen_texts'?
    final_results = []
    seen_texts = set()

    for doc in hybrid_results:
        if doc["text"] not in seen_texts:
            final_results.append(doc)
            seen_texts.add(doc["text"])

    # Return the top 5 combined and deduplicated results
    return final_results[:5]
