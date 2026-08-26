from typing import Literal, Optional

from pydantic import BaseModel


class EvidenceItem(BaseModel):
    citation_id: str

    content: str

    source_id: str

    source_name: str

    source_type: Literal[
        "internal",
        "web",
    ] = "internal"

    chunk_id: Optional[str] = None

    distance: Optional[float] = None

    source_url: Optional[str] = None

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