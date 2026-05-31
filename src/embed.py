# src/embed.py
from sentence_transformers import SentenceTransformer
from src.ingest import extract_pdf_text, chunk_text

def generate_embeddings(chunks: list[str]):
    """
    Loads the bge-m3 model locally and converts a list of text chunks
    into a list of 1024-dimensional mathematical vectors.
    """
    print("Loading embedding model (this may take a minute on first run)...")

    # TODO: beg-m3 is downloaded and referenced using "model" variable.
    model = SentenceTransformer("BAAI/bge-m3")

    print(f"Embedding {len(chunks)} chunks into vector space...")

    # TODO: encodes the chunks using the model i.e M3encodder
    embeddings = model.encode(chunks, show_progress_bar=True)

    return embeddings

if __name__ == "__main__":
    test_pdf = "data/sample.pdf"

    try:
        print("--- STARTING PIPELINE ---")

        # TODO: extracts the text, stores in raw_text, creates chunks of raw_text and storesin text_chunks
        raw_text = extract_pdf_text(test_pdf)
        text_chunks = chunk_text(raw_text)

        # We only process the first 5 chunks to save time during testing.
        test_chunks = text_chunks[:5]

        # TODO: generate vectors of the 5 chunks
        vectors = generate_embeddings(test_chunks)

        print("\n--- EMBEDDING SUCCESSFUL ---")
        print(f"Number of vectors generated: {len(vectors)}")

        # TODO: i don't actually know!
        print(f"Dimensions of the first vector: {len(vectors[0])} (Should be 1024!)")

    except Exception as e:
        print(f"\n[ERROR] Pipeline Failed: {e}")
