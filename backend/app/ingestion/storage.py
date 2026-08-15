import json
from pathlib import Path

from .schemas import NormalizedDocument


def save_documents_jsonl(
    documents: list[NormalizedDocument],
    output_path: Path,
) -> None:
    """
    Save normalized documents as JSON Lines.

    Each document unit is stored as one JSON object per line.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        for document in documents:

            file.write(
                json.dumps(
                    document.model_dump(),
                    ensure_ascii=False,
                )
                + "\n"
            )