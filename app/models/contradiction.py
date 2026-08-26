from typing import List

from pydantic import BaseModel


class Contradiction(BaseModel):
    topic: str

    source_ids: List[str]

    explanation: str


class ContradictionResult(BaseModel):
    contradictions: List[Contradiction]