from pydantic import BaseModel, Field
from typing import Any

class IngestedDocument(BaseModel):
    """Normalized representation of a loaded document after ingestion."""

    document_id: str
    source: str
    file_name: str
    file_path: str
    text: str
    # We're using Python's built-in generic type: dict[str, Any] instead of Dict[str, Any], because we're targeting modern Python.
    metadata: dict[str, Any] = Field(default_factory=dict)

class NormalizedDocument(BaseModel):
    """
    Canonical representation used by downstream ingestion stages.
    """

    document_id: str
    source: str
    file_name: str
    title: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)