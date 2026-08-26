from pathlib import Path
from typing import Optional
from uuid import uuid4

from app.models.document import (
    DocumentMetadata,
    IngestedDocument,
)


def load_text_document(
    file_path: str,
    industry: Optional[str] = None,
    document_type: Optional[str] = None,
) -> IngestedDocument:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    if path.suffix.lower() != ".txt":
        raise ValueError(
            "Only .txt files are supported by this loader."
        )

    content = path.read_text(
        encoding="utf-8"
    )

    if not content.strip():
        raise ValueError(
            "Document contains no readable text."
        )

    metadata = DocumentMetadata(
        source_id=str(uuid4()),
        source_name=path.name,
        industry=industry,
        document_type=document_type,
    )

    return IngestedDocument(
        content=content,
        metadata=metadata
    )