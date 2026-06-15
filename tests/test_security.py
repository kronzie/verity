# tests/test_security.py
import pytest
# We are importing a function from a file we haven't created yet!
from src.security import redact_pii

def test_pii_redaction():
    """
    Unit test to verify that the Presidio security shield successfully
    strips sensitive information before it can be embedded.
    """
    # 1. Define highly sensitive mock data
    raw_text = "My name is John Doe and my secret email is john.doe@enterprise.com. Call me at 555-123-4567."

    # 2. Pass it through the security shield
    sanitized_text = redact_pii(raw_text)

    print(f"\nOriginal: {raw_text}")
    print(f"Sanitized: {sanitized_text}")

    # 3. THE PROFESSIONAL ASSERTIONS (The shield MUST catch these)
    assert "John Doe" not in sanitized_text, "CRITICAL FAILURE: Name was not redacted!"
    assert "john.doe@enterprise.com" not in sanitized_text, "CRITICAL FAILURE: Email was not redacted!"
    assert "555-123-4567" not in sanitized_text, "CRITICAL FAILURE: Phone number was not redacted!"

    # 4. Verify that Presidio inserted its replacement tags
    assert "<PERSON>" in sanitized_text or "<EMAIL_ADDRESS>" in sanitized_text, "FAILURE: Redaction tags are missing."
