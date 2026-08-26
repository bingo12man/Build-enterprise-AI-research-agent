from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
)

from app.models.history import (
    ResearchHistoryItem,
)
from app.repositories.research_repository import (
    get_recent_research,
    get_research_by_id,
)


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get(
    "",
    response_model=List[ResearchHistoryItem],
)
def get_history(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
) -> List[ResearchHistoryItem]:

    rows = get_recent_research(
        limit=limit
    )

    return [
        ResearchHistoryItem(
            **row
        )
        for row in rows
    ]


@router.get(
    "/{research_id}",
    response_model=ResearchHistoryItem,
)
def get_history_item(
    research_id: str,
) -> ResearchHistoryItem:

    row = get_research_by_id(
        research_id
    )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Research record not found.",
        )

    return ResearchHistoryItem(
        **row
    )