from pydantic import BaseModel


class ResearchHistoryItem(BaseModel):
    research_id: str
    query: str
    summary: str
    confidence_level: str
    confidence_explanation: str
    created_at: str