from typing import List

from pydantic import BaseModel


class EvidenceComparison(BaseModel):
    topic: str

    supporting_sources: List[str]

    summary: str


class EvidenceComparisonResult(BaseModel):
    comparisons: List[EvidenceComparison]