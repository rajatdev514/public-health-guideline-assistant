from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.chunking.schemas import DocumentChunk
from app.chunking.utils import generate_chunk_id
from app.ingestion.schemas import NormalizedDocument

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 150

def create_recursive_splitter(chunk_size:int = DEFAULT_CHUNK_SIZE, chunk_overlap:int = DEFAULT_CHUNK_OVERLAP) -> RecursiveCharacterTextSplitter:
    """
    Create the baseline recursive text splitter.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

def chunk_document_recursive(
        document: NormalizedDocument,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> list[DocumentChunk]:
    """
    Split a normalized document unit using recursive chunking.
    """

    splitter = create_recursive_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    split_texts = splitter.split_text(
        document.text
    )

    chunks = []

    for index, text in enumerate(split_texts):
        chunk_id = generate_chunk_id(
            document_id=document.document_id,
            chunk_index=index,
            strategy="recursive"
        )

        metadata = dict(document.metadata)

        metadata.update(
            {
                "chunk_index": index,
                "chunking_strategy": "recursive",
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
            }
        )

        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                text=text,
                source=document.source,
                title=document.title,
                file_name=document.file_name,
                metadata=metadata,
            )
        )

    return chunks