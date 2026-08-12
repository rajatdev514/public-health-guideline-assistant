import re
from collections import Counter

from .schemas import NormalizedDocument

# Matches lines containing only a page number.
# Examples:
# 1
# 25
# 102
PAGE_NUMBER_PATTERN = re.compile(r"^\s*\d{1,4}\s*$")

# Matches spaces/tabs that occur before a newline.
TRAILING_WHITESPACE_PATTERN = re.compile(r"[ \t]+\n")


# Matches 3 or more consecutive blank lines.
EXCESSIVE_NEWLINES_PATTERN = re.compile(r"\n{3,}")

def normalize_line_endings(text: str) -> str:
    """
    Normalize Windows and old-style Mac line endings
    to Unix-style line endings.
    """

    return text.replace("\r\n", "\n").replace("\r", "\n")

def remove_invisible_characters(text: str) -> str:
    """
    Remove null characters and other common invisible
    control characters while preserving newlines and tabs.
    """

    return text.replace("\x00", "")

def normalize_spaces(text: str) -> str:
    """
    Normalize repeated spaces and tabs without flattening
    paragraph or line boundaries.
    """

    lines = text.split("\n")

    normalized_lines = []

    for line in lines:
        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        normalized_lines.append(line)

    return "\n".join(normalized_lines)


def remove_standalone_page_numbers(text: str) -> str:
    """
    Remove lines that contain only a page number.

    This is intentionally conservative so numbers inside
    medical content are not removed.
    """

    lines = text.split("\n")

    cleaned_lines = [
        line
        for line in lines
        if not PAGE_NUMBER_PATTERN.match(line)
    ]

    return "\n".join(cleaned_lines)


def normalize_blank_lines(text: str) -> str:
    """
    Reduce excessive blank lines while preserving paragraph
    separation.
    """

    text = EXCESSIVE_NEWLINES_PATTERN.sub("\n\n", text)

    return text.strip()

def clean_text(text: str) -> str:
    """
    Apply deterministic, conservative text normalization.
    """

    text = normalize_line_endings(text)

    text = remove_invisible_characters(text)

    text = normalize_spaces(text)

    text = remove_standalone_page_numbers(text)

    text = TRAILING_WHITESPACE_PATTERN.sub("\n", text)

    text = normalize_blank_lines(text)

    return text

def clean_document(document: NormalizedDocument) -> NormalizedDocument:
    """
    Clean a single normalized document unit.
    The original object is not modified.
    """

    cleaned_text = clean_text(document.text)

    return document.model_copy(
        update={
            "text": cleaned_text,
        }
    )

def find_repeated_lines(documents: list[NormalizedDocument], minimum_occurrences: int = 3) -> set[str]:
    """
    Identify lines that occur repeatedly across document units.

    Repeated lines are candidates for headers/footers.

    We only identify them here; we do not automatically remove
    them unless they meet additional safety criteria.
    """

    line_counts: Counter[str] = Counter()

    for document in documents:

        # Count a line at most once per document unit.
        unique_lines = {
            line.strip()
            for line in document.text.split("\n")
            if line.strip()
        }

        for line in unique_lines:
            line_counts[line] += 1

    return {
        line
        for line, count in line_counts.items()
        if count >= minimum_occurrences
    }

def remove_repeated_boilerplate(text: str, repeated_lines: set[str]) -> str:
    """
    Remove lines identified as repeated boilerplate.

    Only short, non-content-like lines are considered safe
    candidates for removal.
    """

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:

        stripped_line = line.strip()

        if (
            stripped_line in repeated_lines
            and len(stripped_line) <= 120
        ):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def clean_documents(documents: list[NormalizedDocument]) -> list[NormalizedDocument]:
    """
    Clean a collection of normalized document units.
    """

    cleaned_documents = []

    for document in documents:
        cleaned_documents.append(
            clean_document(document)
        )

    return cleaned_documents