from fastapi import APIRouter

from app.models.research import ResearchRequest, ResearchResponse

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@router.post(
    "/research",
    response_model=ResearchResponse
)
def research(request: ResearchRequest):
    return ResearchResponse(
        query=request.query,
        message="Research request received"
    )