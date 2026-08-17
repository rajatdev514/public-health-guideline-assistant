from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator

class ChunkingConfig(BaseModel):
    """
    Configuration for a chunking experiment.
    """

    strategy: Literal["recursive", "semantic"] = "recursive"

    chunk_size: int = Field(
        default=1000,
        gt=0
    )

    chunk_overlap: int = Field(
        default=150,
        gt=0
    )

    @model_validator(mode="after")
    def validate_overlap(self):
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )
        return self

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