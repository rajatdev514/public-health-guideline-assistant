from pathlib import Path

from app.ingestion.pipeline import process_dataset
from app.ingestion.storage import save_documents_jsonl


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIRECTORY = PROJECT_ROOT / "datasets" / "raw"

PROCESSED_DIRECTORY = (
    PROJECT_ROOT / "datasets" / "processed"
)

OUTPUT_FILE = (
    PROCESSED_DIRECTORY / "documents.jsonl"
)


def main():
    print("=" * 60)
    print("Public Health Guideline Assistant")
    print("Document Ingestion")
    print("=" * 60)

    print(f"\nRaw dataset: {RAW_DIRECTORY}")

    documents = process_dataset(
        RAW_DIRECTORY
    )

    print(
        f"\nValid document units: "
        f"{len(documents)}"
    )

    save_documents_jsonl(
        documents,
        OUTPUT_FILE,
    )

    print(
        f"\nProcessed documents saved to:"
    )

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()