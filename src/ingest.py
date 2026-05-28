import pdfplumber
import os

def extract_pdf_text(pdf_path: str) -> str:
    """
    Opens a PDF document, iterates through every page, extracts the raw layout text,
    strips out standard header noise, and returns a single unified string.
    """
    # 1. Initialize an empty container to hold text from all pages
    full_text = []

    # 2. Check if the file actually exists on the path before opening it
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Target PDF file not found at: {pdf_path}")

    # 3. Use pdfplumber's safe context manager to unlock the file
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through pages using a structured loop
        for page_num, page in enumerate(pdf.pages, start=1):

            # Extract text with layout analysis enabled
            text = page.extract_text(layout=False)

            if text:
                # Basic cleaning: remove trailing white spaces on lines
                cleaned_text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])
                full_text.append(cleaned_text)

    # 4. Join all pages into a single cohesive string asset
    return "\n\n".join(full_text)

# This block allows us to run this file directly to test it!
if __name__ == "__main__":
    # 1. Define the path to your test PDF
    # (Make sure you put a real PDF in the data folder and name it 'sample.pdf')
    test_pdf_path = "data/sample.pdf"

    print(f"Attempting to extract text from: {test_pdf_path}...")

    try:
        # 2. Run the extraction engine
        extracted_text = extract_pdf_text(test_pdf_path)

        # 3. Print the results (just the first 1000 characters so it doesn't flood the terminal)
        print("\n--- EXTRACTION SUCCESSFUL ---")
        print(f"Total Characters Extracted: {len(extracted_text)}")
        print("\n--- PREVIEW (First 1000 chars) ---")
        print(extracted_text[:1000])

    except Exception as e:
        print(f"\n[ERROR] Pipeline Failed: {e}")
