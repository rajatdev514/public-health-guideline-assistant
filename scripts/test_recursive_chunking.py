from pathlib import Path

from app.chunking.recursive import (
    chunk_document_recursive,
)
from app.ingestion.loaders import load_file
from app.ingestion.parser import parse_document
from app.ingestion.cleaner import clean_documents


RAW_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "datasets"
    / "raw"
)


def main():

    pdf_files = list(
        RAW_DIRECTORY.rglob("*.pdf")
    )

    if not pdf_files:
        print("No PDF files found.")
        return

    file_path = pdf_files[0]

    print(f"Testing: {file_path}")

    loaded_documents = load_file(
        file_path
    )

    normalized_documents = [
        parse_document(document)
        for document in loaded_documents
    ]

    cleaned_documents = clean_documents(
        normalized_documents
    )

    document = cleaned_documents[0]

    chunks = chunk_document_recursive(
        document
    )

    print(
        f"\nOriginal characters: "
        f"{len(document.text)}"
    )

    print(
        f"Generated chunks: "
        f"{len(chunks)}"
    )

    for chunk in chunks[:5]:

        print("\n" + "=" * 70)

        print(
            f"Chunk ID: {chunk.chunk_id}"
        )

        print(
            f"Page: "
            f"{chunk.metadata.get('page')}"
        )

        print(
            f"Chunk index: "
            f"{chunk.metadata.get('chunk_index')}"
        )

        print(
            f"Characters: "
            f"{len(chunk.text)}"
        )

        print("\nText:")

        print(chunk.text)


if __name__ == "__main__":
    main()