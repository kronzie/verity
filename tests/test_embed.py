# tests/test_embed.py
import os
import shutil
import pytest
import chromadb
# We are importing a function that we haven't written yet!
from src.embed import save_to_vectorstore

def test_chromadb_storage():
    """
    Unit test to verify that vectors and text chunks are correctly
    committed to the local persistent storage layer.
    """
    # 1. Define mock input data
    mock_chunks = ["Artificial Intelligence is changing software development."]
    mock_vectors = [[0.1] * 1024] # A fake 1024-dimensional vector
    mock_metadata = [{"clearance_level": "standard", "source": "test_doc.pdf"}]
    test_db_dir = "./vectorstore_test"

    # 2. Call the production function (which will create the DB and save the data)
    save_to_vectorstore(mock_chunks, mock_vectors, mock_metadata, persist_directory=test_db_dir)

    # 3. Initialize a local ChromaDB client to inspect the test directory
    client = chromadb.PersistentClient(path=test_db_dir)
    collection = client.get_collection(name="verity_docs")

    # 4. Pull the data back out of the database
    results = collection.get(ids=["doc_0"])

    # 5. THE PROFESSIONAL ASSERTIONS (If any of these are false, the test fails)
    assert len(results['documents']) == 1, "Failed: Document was not saved."
    assert results['documents'][0] == mock_chunks[0], "Failed: Text was corrupted during save."
    assert results['metadatas'][0]['clearance_level'] == "standard", "Failed: RBAC metadata lost."

    # 6. Clean up the test database directory after the test runs
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)
