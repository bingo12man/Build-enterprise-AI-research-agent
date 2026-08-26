from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Business research question"
    )

    industry: Optional[str] = Field(
        default=None,
        description="Optional industry filter"
    )

    document_type: Optional[str] = Field(
        default=None,
        description="Optional document type filter"
    )

    date_from: Optional[date] = Field(
        default=None,
        description="Only consider documents from this date onward"
    )


class SourceReference(BaseModel):
    source_id: str
    source_name: str
    evidence_text: str

    source_type: str

    source_url: Optional[str] = None


class Finding(BaseModel):
    title: str
    description: str
    source_ids: list[str]


class Opportunity(BaseModel):
    title: str
    description: str
    expected_value: Literal["Low", "Medium", "High"]
    difficulty: Literal["Low", "Medium", "High"]
    source_ids: list[str]


class Risk(BaseModel):
    title: str
    description: str
    source_ids: list[str]


class EvidenceConfidence(BaseModel):
    level: Literal["Low", "Medium", "High"]
    explanation: str


class ResearchResponse(BaseModel):
    research_id: str
    query: str
    summary: str
    findings: list[Finding]
    opportunities: list[Opportunity]
    risks: list[Risk]
    sources: list[SourceReference]
    confidence: EvidenceConfidence