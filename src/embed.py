# src/embed.py
import chromadb
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

def save_to_vectorstore(chunks: list[str], embeddings: list[list[float]], metadata: list[dict], persist_directory: str = "vectorstore"):
    """
    Takes text chunks, their mathematical vectors, and RBAC metadata,
    and saves them permanently to the hard drive using ChromaDB.
    """
    print(f"Connecting to ChromaDB at ./{persist_directory} ...")

    # TODO 1: PersistentClient is intended for local development and testing. Also there is EphemeralClient which stores all data in memory for testing, shouldn't we be using EphemeralClient?
    client = chromadb.PersistentClient(path=persist_directory)

    # TODO 2: Collections are the fundamental unit of storage and querying in Chroma.
    collection = client.get_or_create_collection(name="verity_docs")

    # TODO 3: I wasn't able to find it.
    ids = [f"doc_{i}" for i in range(len(chunks))]

    print("Writing data to disk...")

    # TODO 4: Please explain, i found .add is used to add a new record to the collection, documents is a string[] var
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
        ids=ids
    )
    print("Successfully saved to ChromaDB!")
    return True

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
