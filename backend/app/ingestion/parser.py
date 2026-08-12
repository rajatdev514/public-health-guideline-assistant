from pathlib import Path
from .schemas import IngestedDocument, NormalizedDocument

def infer_source(file_path: str) -> str:
    """
    Infer the document source from the directory structure.

    Example:
        datasets/raw/who/document.pdf
        -> WHO
    """

    path = Path(file_path)

    parts = [part.lower() for part in path.parts]

    if "who" in parts:
        return "WHO"

    if "cdc" in parts:
        return "CDC"

    if "ndep" in parts:
        return "NDEP"

    if "research" in parts:
        return "Research"

    return "Unknown"

def infer_title(file_name: str) -> str:
    """
    Create a readable title from the filename.

    Example:
        WHO_TB_Guideline_2024.pdf
        -> WHO TB Guideline 2024
    """

    title = Path(file_name).stem

    title = title.replace("_", " ")
    title = title.replace("-", " ")

    return " ".join(title.split())

def parse_document(document: IngestedDocument,) -> NormalizedDocument:
    """
    Convert a loader output into the application's
    canonical document representation.
    """

    source = infer_source(document.file_path)
    title = infer_title(document.file_name)

    metadata = dict(document.metadata)

    metadata.update(
        {
            "source": source,
            "title": title,
            "document_id": document.document_id,
            "file_name": document.file_name,
        }
    )

    return NormalizedDocument(
        document_id=document.document_id,
        source=source,
        file_name=document.file_name,
        title=title,
        text=document.text,
        metadata=metadata,
    )