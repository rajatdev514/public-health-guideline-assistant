from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.chunking.schemas import ChunkingConfig, DocumentChunk
from app.chunking.utils import generate_chunk_id
from app.ingestion.schemas import NormalizedDocument


def create_recursive_splitter(config: ChunkingConfig) -> RecursiveCharacterTextSplitter:
    """
    Create a recursive text splitter from configuration.
    """

    if config.strategy != "recursive":
        raise ValueError(
            "Recursive splitter requires "
            "strategy='recursive'"
        )

    return RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
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


def chunk_document_recursive(document: NormalizedDocument,config: ChunkingConfig) -> list[DocumentChunk]:
    """
    Split a normalized document using recursive chunking.
    """

    splitter = create_recursive_splitter(
        config
    )

    split_texts = splitter.split_text(
        document.text
    )

    chunks = []

    for index, text in enumerate(split_texts):
        chunk_id = generate_chunk_id(
            document_id=document.document_id,
            chunk_index=index,
            strategy=config.strategy,
        )

        metadata = dict(document.metadata)

        metadata.update(
            {
                "chunk_index": index,
                "chunking_strategy": config.strategy,
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
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