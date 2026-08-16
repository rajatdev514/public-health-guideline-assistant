import hashlib

def generate_chunk_id(document_id: str, chunk_index: int, strategy: str) -> str:
    """
    Generate a deterministic chunk ID
    """

    raw_id = (
        f"{document_id}:"
        f"{strategy}:"
        f"{chunk_index}:"
    )

    digest = hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()

    return digest[:20]