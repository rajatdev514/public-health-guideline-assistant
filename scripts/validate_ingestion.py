import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "documents.jsonl"
)

# A unit shorter than this is suspicious.
MINIMUM_EXPECTED_CHARACTERS = 50


def load_documents() -> list[dict]:
    """
    Load processed document units from JSONL.
    """

    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {PROCESSED_FILE}"
        )

    documents = []

    with PROCESSED_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                documents.append(
                    json.loads(line)
                )

            except json.JSONDecodeError as exc:
                print(
                    f"WARNING: Invalid JSON "
                    f"on line {line_number}: {exc}"
                )

    return documents


def calculate_statistics(
    documents: list[dict],
) -> dict:

    character_counts = [
        len(document.get("text", "").strip())
        for document in documents
    ]

    empty_units = [
        document
        for document in documents
        if not document.get("text", "").strip()
    ]

    short_units = [
        document
        for document in documents
        if 0 < len(document.get("text", "").strip())
        < MINIMUM_EXPECTED_CHARACTERS
    ]

    sources = Counter(
        document.get("source", "Unknown")
        for document in documents
    )

    files = {
        document.get(
            "file_name",
            "Unknown",
        )
        for document in documents
    }

    return {
        "files": len(files),
        "units": len(documents),
        "empty_units": len(empty_units),
        "short_units": len(short_units),
        "total_characters": sum(character_counts),
        "average_characters": (
            sum(character_counts) / len(character_counts)
            if character_counts
            else 0
        ),
        "minimum_characters": (
            min(character_counts)
            if character_counts
            else 0
        ),
        "maximum_characters": (
            max(character_counts)
            if character_counts
            else 0
        ),
        "sources": dict(sources),
    }


def find_duplicate_units(
    documents: list[dict],
) -> list[dict]:

    text_counts = Counter(
        document.get("text", "").strip()
        for document in documents
        if document.get("text", "").strip()
    )

    duplicates = []

    for text, count in text_counts.items():

        if count > 1:

            duplicates.append(
                {
                    "occurrences": count,
                    "text_preview": text[:150],
                }
            )

    return duplicates


def validate_metadata(
    documents: list[dict],
) -> dict:

    missing_source = []
    missing_document_id = []
    missing_page = []

    for document in documents:

        if not document.get("source"):
            missing_source.append(
                document.get("file_name")
            )

        if not document.get("document_id"):
            missing_document_id.append(
                document.get("file_name")
            )

        metadata = document.get(
            "metadata",
            {},
        )

        # Page is expected for PDF page-level units.
        if (
            document.get("file_name", "")
            .lower()
            .endswith(".pdf")
            and "page" not in metadata
        ):
            missing_page.append(
                document.get("file_name")
            )

    return {
        "missing_source": missing_source,
        "missing_document_id": missing_document_id,
        "missing_page": missing_page,
    }


def print_report(
    statistics: dict,
    duplicates: list[dict],
    metadata_issues: dict,
) -> None:

    print("\n")
    print("=" * 70)
    print("PUBLIC HEALTH GUIDELINE ASSISTANT")
    print("INGESTION QUALITY REPORT")
    print("=" * 70)

    print("\nCorpus Statistics")
    print("-" * 70)

    print(
        f"Source files:              "
        f"{statistics['files']}"
    )

    print(
        f"Document units/pages:      "
        f"{statistics['units']}"
    )

    print(
        f"Empty units:               "
        f"{statistics['empty_units']}"
    )

    print(
        f"Short units:               "
        f"{statistics['short_units']}"
    )

    print(
        f"Total characters:          "
        f"{statistics['total_characters']:,}"
    )

    print(
        f"Average characters/unit:   "
        f"{statistics['average_characters']:.2f}"
    )

    print(
        f"Minimum characters/unit:   "
        f"{statistics['minimum_characters']}"
    )

    print(
        f"Maximum characters/unit:   "
        f"{statistics['maximum_characters']}"
    )

    print("\nSources")
    print("-" * 70)

    for source, count in statistics["sources"].items():

        print(
            f"{source:<25} {count}"
        )

    print("\nMetadata Validation")
    print("-" * 70)

    print(
        f"Missing source:            "
        f"{len(metadata_issues['missing_source'])}"
    )

    print(
        f"Missing document ID:       "
        f"{len(metadata_issues['missing_document_id'])}"
    )

    print(
        f"PDF units missing page:    "
        f"{len(metadata_issues['missing_page'])}"
    )

    print("\nDuplicate Units")
    print("-" * 70)

    print(
        f"Duplicate text groups:     "
        f"{len(duplicates)}"
    )

    print("\nQuality Status")
    print("-" * 70)

    has_issues = (
        statistics["empty_units"] > 0
        or len(metadata_issues["missing_source"]) > 0
        or len(metadata_issues["missing_document_id"]) > 0
    )

    if has_issues:
        print("WARNING: Dataset requires attention.")

    else:
        print("PASS: No critical ingestion issues detected.")

    print("=" * 70)


def main():

    print(
        f"Reading processed dataset:\n"
        f"{PROCESSED_FILE}"
    )

    documents = load_documents()

    if not documents:
        print(
            "\nNo processed documents found."
        )
        return

    statistics = calculate_statistics(
        documents
    )

    duplicates = find_duplicate_units(
        documents
    )

    metadata_issues = validate_metadata(
        documents
    )

    save_report(
        statistics,
        duplicates,
        metadata_issues,
    )

    print_report(
        statistics,
        duplicates,
        metadata_issues,
    )

def save_report(
    statistics: dict,
    duplicates: list[dict],
    metadata_issues: dict,
) -> None:

    report = {
        "statistics": statistics,
        "duplicates": duplicates,
        "metadata_issues": metadata_issues,
    }

    output_path = (
        PROJECT_ROOT
        / "docs"
        / "ingestion_report.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nReport saved to: {output_path}"
    )


if __name__ == "__main__":
    main()