from typing import Any
from pydantic import BaseModel, Field

class DocumentChunk(BaseModel):
    """
    Represents a retrievable chunk derived from a normalized document.
    """

    chunk_id: str
    document_id: str
    text: str
    source: str
    title: str
    file_name: str

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )