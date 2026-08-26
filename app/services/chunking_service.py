from typing import List
from uuid import uuid4

from app.models.document import (
    DocumentChunk,
    IngestedDocument,
)


def chunk_document(
    document: IngestedDocument,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> List[DocumentChunk]:

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text = document.content

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    content=chunk_text,
                    metadata=document.metadata,
                )
            )

        start = end - chunk_overlap

    return chunks