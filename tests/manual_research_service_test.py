from app.models.research import (
    ResearchRequest,
)
from app.services.research_service import (
    run_research,
)


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


print("\nRESEARCH ID")
print(result.research_id)


print("\nSUMMARY")
print(result.summary)


print("\nFINDINGS")

for item in result.findings:
    print(
        "-",
        item.title,
        item.source_ids,
    )


print("\nOPPORTUNITIES")

for item in result.opportunities:
    print(
        "-",
        item.title,
        item.expected_value,
        item.source_ids,
    )


print("\nRISKS")

for item in result.risks:
    print(
        "-",
        item.title,
        item.source_ids,
    )


print("\nSOURCES")

for source in result.sources:
    print(
        "-",
        source.source_id,
        source.source_name,
    )


print("\nCONFIDENCE")
print(result.confidence.level)
print(
    result.confidence.explanation
)