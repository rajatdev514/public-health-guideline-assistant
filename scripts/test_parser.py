from pathlib import Path

from app.ingestion.loaders import load_file
from app.ingestion.parser import parse_document


RAW_DATASET_PATH = Path("datasets/raw")


def main():
    pdf_files = list(RAW_DATASET_PATH.rglob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    file_path = pdf_files[0]

    print(f"Parsing: {file_path}")

    loaded_documents = load_file(file_path)

    print(f"Loaded units: {len(loaded_documents)}")

    normalized_documents = [
        parse_document(document)
        for document in loaded_documents
    ]

    for document in normalized_documents[:3]:

        print("\n--- Normalized Document ---")

        print("Document ID:", document.document_id)
        print("Source:", document.source)
        print("Title:", document.title)
        print("File:", document.file_name)
        print("Metadata:", document.metadata)

        print("\nText preview:")
        print(document.text[:500])


if __name__ == "__main__":
    main()