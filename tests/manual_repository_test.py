from app.models.research import (
    ResearchRequest,
)
from app.repositories.research_repository import (
    get_recent_research,
    initialize_database,
)
from app.services.research_service import (
    run_research,
)


initialize_database()


request = ResearchRequest(
    query=(
        "What AI opportunities can help "
        "a manufacturing company?"
    ),
    industry="manufacturing",
)


result = run_research(
    request
)


print(
    "Created research:",
    result.research_id,
)


history = get_recent_research(
    limit=5
)


print("\nRECENT HISTORY")


for item in history:
    print("\n--------------------")
    print(
        "Research ID:",
        item["research_id"],
    )
    print(
        "Query:",
        item["query"],
    )
    print(
        "Confidence:",
        item["confidence_level"],
    )
    print(
        "Created:",
        item["created_at"],
    )