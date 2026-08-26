from datetime import date
from typing import Optional

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    source_id: str
    source_name: str
    document_type: Optional[str] = None
    industry: Optional[str] = None
    published_date: Optional[date] = None


class IngestedDocument(BaseModel):
    content: str
    metadata: DocumentMetadata


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: DocumentMetadata