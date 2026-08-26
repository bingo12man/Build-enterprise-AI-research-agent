from app.services.llm_service import (
    generate_research_result,
)
from app.services.retrieval_service import (
    retrieve_evidence,
)
from app.services.validation_service import (
    validate_citations,
)


query = (
    "What AI opportunities can help "
    "a manufacturing company?"
)


evidence = retrieve_evidence(
    query=query,
    top_k=3,
    industry="manufacturing",
)


result = generate_research_result(
    query=query,
    evidence_items=evidence,
)


validation = validate_citations(
    result=result,
    evidence_items=evidence,
)


print(
    "Validation passed:",
    validation.is_valid
)


if validation.errors:
    print("\nERRORS")

    for error in validation.errors:
        print(
            "-",
            error
        )