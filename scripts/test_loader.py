from pathlib import Path

from app.ingestion.loaders import load_file


RAW_DATASET_PATH = Path("datasets/raw")


def main():
    pdf_files = list(RAW_DATASET_PATH.rglob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    for pdf_file in pdf_files:

        print(f"\nLoading: {pdf_file}")

        documents = load_file(pdf_file)

        print(f"Loaded units: {len(documents)}")

        for document in documents[:3]:

            print("\n--- Document Unit ---")

            print("Document ID:", document.document_id)
            print("File:", document.file_name)
            print("Metadata:", document.metadata)

            print("\nText preview:")
            print(document.text[:500])


if __name__ == "__main__":
    main()