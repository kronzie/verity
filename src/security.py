# src/security.py
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

print("Loading Microsoft Presidio NLP Security Engines...")
# We initialize the engines outside the function so they only load into memory once,
# instead of reloading every time we pass a new chunk of text.
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def redact_pii(text: str) -> str:
    """
    Scans raw text for Personally Identifiable Information (PII)
    and replaces it with safe <TAGS> before embedding.
    """
    # TODO 1: We need to be able to recognize sensitive data, if it fails to analyze these data then those dat would be leaked.
    results = analyzer.analyze(text=text, language='en')

    # TODO 2: currently results entities such as credit card, email, ip & mac address, location and for india pan, aadhaar, etc or wait am i explaining something else here?

    # TODO 3: I found there are various operations you can do on the recognized text with the anonymize function such as replace, redact, hash, encrypt, etc. but this code line doesn't seem to use any of them so I am not sure of the result
    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=results)

    return anonymized_result.text
