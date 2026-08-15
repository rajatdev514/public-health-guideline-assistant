# Its responsibilities:

# Find supported files.
# Load each file.
# Parse each loaded unit.
# Clean the text.
# Validate the result.
# Return the processed documents.


from pathlib import Path
from .cleaner import clean_document, validate_document
from .loaders import SUPPORTED_EXTENSIONS, load_file
from .parser import parse_document
from .schemas import NormalizedDocument

def discover_files(raw_directory: Path) -> list[Path]:
    """
    Recursively discover all supported documents
    under the raw dataset directory.
    """

    files = []

    for file_path in raw_directory.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(file_path)\

    return sorted(files)

def process_file(file_path: Path) -> list[NormalizedDocument]:
    """
    Run the complete ingestion process for one file.
    Flow: Load → Parse → Clean → Validate
    """

    loaded_documents = load_file(file_path)

    normalized_documents = [
        parse_document(document)
        for document in loaded_documents
    ]

    cleaned_documents = [
        clean_document(document)
        for document in normalized_documents
    ]

    validate_documents = [
        document
        for document in cleaned_documents
        if validate_document(document)
    ]

    return validate_documents

def process_dataset(raw_directory: Path) -> list[NormalizedDocument]:
    """
    Process every supported document in the raw dataset
    """

    files = discover_files(raw_directory)

    all_documents: list[NormalizedDocument] = []

    for file_path in files:
        documents = process_file(file_path)
        all_documents.extend(documents)

    return all_documents