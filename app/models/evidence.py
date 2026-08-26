from typing import List, Literal, Optional

from pydantic import BaseModel


class EvidenceItem(BaseModel):
    citation_id: str
    chunk_id: str
    content: str
    source_id: str
    source_name: str
    distance: float
    industry: Optional[str] = None
    document_type: Optional[str] = None


class EvidenceAssessment(BaseModel):
    level: Literal[
        "Low",
        "Medium",
        "High",
    ]
    explanation: str
    average_distance: Optional[float] = None
    evidence_count: int
    unique_source_count: int