from pathlib import Path

from app.ingestion.cleaner import (
    clean_documents,
    find_repeated_lines,
)
from app.ingestion.loaders import load_file
from app.ingestion.parser import parse_document


RAW_DATASET_PATH = Path("datasets/raw")


def main():

    pdf_files = list(
        RAW_DATASET_PATH.rglob("*.pdf")
    )

    if not pdf_files:
        print("No PDF files found.")
        return

    file_path = pdf_files[0]

    print(f"Processing: {file_path}")

    # -----------------------------
    # Load
    # -----------------------------

    loaded_documents = load_file(file_path)

    print(
        f"Loaded units: {len(loaded_documents)}"
    )

    # -----------------------------
    # Parse
    # -----------------------------

    normalized_documents = [
        parse_document(document)
        for document in loaded_documents
    ]

    # -----------------------------
    # Detect repeated lines
    # -----------------------------

    repeated_lines = find_repeated_lines(
        normalized_documents
    )

    print(
        f"\nRepeated lines found: "
        f"{len(repeated_lines)}"
    )

    for line in list(repeated_lines)[:10]:
        print(f"  - {line}")

    # -----------------------------
    # Clean
    # -----------------------------

    cleaned_documents = clean_documents(
        normalized_documents
    )

    # -----------------------------
    # Compare
    # -----------------------------

    original = normalized_documents[0]
    cleaned = cleaned_documents[0]

    print("\n==============================")
    print("ORIGINAL TEXT")
    print("==============================")

    print(original.text[:1000])

    print("\n==============================")
    print("CLEANED TEXT")
    print("==============================")

    print(cleaned.text[:1000])


if __name__ == "__main__":
    main()