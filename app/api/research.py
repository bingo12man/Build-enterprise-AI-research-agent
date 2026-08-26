from fastapi import (
    APIRouter,
    HTTPException,
)

from app.models.exceptions import (
    LLMServiceError,
    RetrievalError,
    ValidationError,
)
from app.models.research import (
    ResearchRequest,
    ResearchResponse,
)
from app.services.research_service import (
    run_research,
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "",
    response_model=ResearchResponse,
)
def create_research(
    request: ResearchRequest,
) -> ResearchResponse:

    try:
        return run_research(
            request
        )

    except RetrievalError:
        raise HTTPException(
            status_code=503,
            detail=(
                "Research retrieval is "
                "temporarily unavailable."
            ),
        )

    except LLMServiceError:
        raise HTTPException(
            status_code=503,
            detail=(
                "AI generation is "
                "temporarily unavailable."
            ),
        )

    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail=(
                "AI response failed "
                "validation."
            ),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected server "
                "error occurred."
            ),
        )