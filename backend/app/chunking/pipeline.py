import json
from pathlib import Path

from app.chunking.recursive import (chunk_document_recursive)
from app.chunking.schemas import (ChunkingConfig, DocumentChunk)
from app.ingestion.schemas import NormalizedDocument

def load_documents_from_jsonl(input_path: Path,) -> list[NormalizedDocument]:
    """
    Load normalized documents from JSONL.
    """

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    documents = []

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            data = json.loads(line)

            documents.append(
                NormalizedDocument.model_validate(
                    data
                )
            )

    return documents

def chunk_documents(documents: list[NormalizedDocument], config: ChunkingConfig) -> list[DocumentChunk]:
    """
     Chunk all normalized documents using the configured strategy
    """ 

    if config.strategy == "recursive":
        chunks = []

        for document in documents:
            document_chunk = (
                chunk_document_recursive(
                    document,
                    config
                )
            )

            chunks.extend(
                document_chunk
            )

        return chunks

    raise NotImplementedError(
        f"Chunking Strategy"
        f"'{config.strategy}' is not implemented yet"
    )

def save_chunks_jsonl(chunks: list[DocumentChunk], output_path: Path) -> None:
    """
    Save generated chunks as JSONL.
    """

    output_path.parent.mkdir(
        parents = True,
        exist_ok = True
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:
        for chunk in chunks:
           file.write(
               json.dumps(
                   chunk.model_dump(),
                   ensure_ascii=False
               )
               + "\n"
           ) 