import pdfplumber
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

# --- NEW FUNCTION (BOX 2) ---
def chunk_text(text: str) -> list[str]:
    """
    Slices a massive string into overlapping 1000-character chunks to preserve
    context for the vector database.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        # 1000 characters per chunk is roughly 250 words
        chunk_size=1000,
        # Overlap by 200 characters so context isn't lost at the boundaries
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    # This splits our giant string into a Python List containing many smaller strings
    chunks = text_splitter.split_text(text)
    return chunks

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    test_pdf_path = "data/sample.pdf"

    try:
        # 1. Run Box 1
        print(f"Extracting text from: {test_pdf_path}...")
        extracted_text = extract_pdf_text(test_pdf_path)

        # 2. Run Box 2
        print("Slicing text into chunks...")
        text_chunks = chunk_text(extracted_text)

        print("\n--- PIPELINE SUCCESSFUL ---")
        print(f"Total Characters: {len(extracted_text)}")
        print(f"Total Chunks Created: {len(text_chunks)}")

        # 3. Print the 3rd chunk just to verify it looks correct
        print("\n--- PREVIEW (Chunk #3) ---")
        if len(text_chunks) >= 3:
            print(text_chunks[2])
        else:
            print("Not enough text to make 3 chunks!")

    except Exception as e:
        print(f"\n[ERROR] Pipeline Failed: {e}")
