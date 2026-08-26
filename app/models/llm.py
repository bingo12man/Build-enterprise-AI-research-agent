from typing import List, Literal

from pydantic import BaseModel


class LLMFinding(BaseModel):
    title: str
    description: str
    source_ids: List[str]


class LLMOpportunity(BaseModel):
    title: str
    description: str
    expected_value: Literal[
        "Low",
        "Medium",
        "High",
    ]
    difficulty: Literal[
        "Low",
        "Medium",
        "High",
    ]
    source_ids: List[str]


class LLMRisk(BaseModel):
    title: str
    description: str
    source_ids: List[str]


class LLMEvidenceConfidence(BaseModel):
    level: Literal[
        "Low",
        "Medium",
        "High",
    ]
    explanation: str


class LLMResearchResult(BaseModel):
    summary: str
    findings: List[LLMFinding]
    opportunities: List[LLMOpportunity]
    risks: List[LLMRisk]
    source_ids: List[str]
    confidence: LLMEvidenceConfidence