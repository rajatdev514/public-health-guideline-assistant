import argparse
from pathlib import Path

from app.chunking.pipeline import (
    chunk_documents,
    load_documents_from_jsonl,
    save_chunks_jsonl,
)
from app.chunking.schemas import ChunkingConfig


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

DEFAULT_INPUT = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "documents.jsonl"
)

# DEFAULT_OUTPUT = (
#     PROJECT_ROOT
#     / "datasets"
#     / "processed"
#     / "chunks_recursive.jsonl"
# )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Chunk normalized public health "
            "guideline documents."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to normalized documents JSONL.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path for generated chunks JSONL.",
    )

    parser.add_argument(
        "--strategy",
        choices=["recursive", "semantic"],
        default="recursive",
        help="Chunking strategy.",
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Maximum chunk size.",
    )

    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=150,
        help="Chunk overlap.",
    )

    return parser.parse_args()

def main():

    args = parse_arguments()

    if args.output is None:
        output_path = (
            PROJECT_ROOT
            / "datasets"
            / "processed"
            / (
                f"chunks_"
                f"{args.strategy}_"
                f"{args.chunk_size}_"
                f"{args.chunk_overlap}"
                f".jsonl"
            )
        )
    else:
        output_path = args.output

    config = ChunkingConfig(
        strategy=args.strategy,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )

    print("=" * 60)
    print("Public Health Guideline Assistant")
    print("Chunking Pipeline")
    print("=" * 60)

    print(
        f"\nStrategy: {config.strategy}"
    )

    print(
        f"Chunk size: {config.chunk_size}"
    )

    print(
        f"Chunk overlap: {config.chunk_overlap}"
    )

    print(
        f"\nInput: {args.input}"
    )

    documents = load_documents_from_jsonl(
        args.input
    )

    print(
        f"Documents loaded: "
        f"{len(documents)}"
    )

    chunks = chunk_documents(
        documents,
        config,
    )

    print(
        f"Chunks generated: "
        f"{len(chunks)}"
    )

    save_chunks_jsonl(
        chunks,
        output_path,
    )

    print(
        f"\nChunks saved to:"
    )

    print(output_path)


if __name__ == "__main__":
    main()