from hashlib import sha256
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
)

from .schemas import IngestedDocument

# Supported file extensions for the ingestion pipeline.
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".html",
    ".htm",
    ".md",
    ".markdown",
}


def generate_document_id(file_path: Path) -> str:
    """Generate a deterministic document ID from a file path."""

    # Normalize the path to ensure the ID is stable across different OS path styles.
    normalized_path = str(file_path.resolve()).lower()
    return sha256(normalized_path.encode("utf-8")).hexdigest()[:16]


def load_file(file_path: Path) -> list[IngestedDocument]:
    """Load a supported document and transform it into IngestedDocument objects."""

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    document_id = generate_document_id(file_path)

    # Select the LangChain loader based on the file extension.
    if extension == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif extension == ".docx":
        loader = UnstructuredWordDocumentLoader(str(file_path))
    elif extension in {".html", ".htm"}:
        loader = UnstructuredHTMLLoader(str(file_path))
    elif extension in {".md", ".markdown"}:
        loader = UnstructuredMarkdownLoader(str(file_path))
    else:
        raise ValueError(f"No loader configured for: {extension}")

    loaded_documents = loader.load()

    results: list[IngestedDocument] = []

    for index, document in enumerate(loaded_documents):
        # Copy document metadata and enrich it with ingestion-specific fields.
        metadata = dict(document.metadata)
        metadata.update(
            {
                "file_type": extension,
                "unit_type": index,
            }
        )

        # Preserve PDF page numbering as 1-based when the loader provides a page field.
        if "page" in metadata:
            metadata["page"] = metadata["page"] + 1

        results.append(
            IngestedDocument(
                document_id=document_id,
                source=metadata.get("source", file_path.name),
                file_name=file_path.name,
                file_path=str(file_path),
                text=document.page_content,
                metadata=metadata,
            )
        )

    return results
