# tests/test_router.py
import pytest
from src.router import dual_engine_retrieve

def test_hybrid_retrieval_and_security_filtering():
    """
    Verifies that the dual-engine router combines semantic and keyword matches,
    and strictly filters out documents above the user's security clearance.
    """
    # 1. Define a mock database list of text chunks with metadata
    # Some chunks are standard clearance, one is top-secret
    mock_corpus = [
        {"text": "System configuration error code 405 detected in server logs.", "clearance": "standard"},
        {"text": "To mitigate model hallucinations, apply advanced retrieval guardrails.", "clearance": "standard"},
        {"text": "CRITICAL SECURITY: Enterprise master encryption keys are stored in Vault X9.", "clearance": "top_secret"},
        {"text": "The server failed with a standard connection timeout error code 405.", "clearance": "standard"}
    ]

    # 2. Test Case A: A user with 'standard' clearance searches for 'error code 405'
    # They should get keyword matches, but NOT the top_secret vault chunk
    query_1 = "error code 405"
    results_standard = dual_engine_retrieve(query=query_1, clearance="standard", corpus=mock_corpus)

    print(f"\nStandard Clearance Results for '{query_1}':")
    for r in results_standard:
        print(f"- {r['text']} (Clearance: {r['clearance']})")

    # Assertions for Standard User
    assert len(results_standard) > 0
    assert any("405" in r["text"] for r in results_standard), "Failure: BM25 failed to prioritize exact matching codes."
    for r in results_standard:
        assert r["clearance"] != "top_secret", "SECURITY BREACH: Standard user retrieved a top_secret document!"

    # 3. Test Case B: A user with 'top_secret' clearance searches for 'encryption keys'
    query_2 = "encryption keys"
    results_secret = dual_engine_retrieve(query=query_2, clearance="top_secret", corpus=mock_corpus)

    # Assertions for Top Secret User
    assert any("master encryption keys" in r["text"] for r in results_secret), "Failure: Secret user could not retrieve secret files."
