from app.models.llm import (
    LLMEvidenceConfidence,
    LLMFinding,
    LLMResearchResult,
)
from app.services.retrieval_service import (
    retrieve_evidence,
)
from app.services.validation_service import (
    validate_citations,
)


query = (
    "How can AI help manufacturing?"
)


evidence = retrieve_evidence(
    query=query,
    top_k=3,
    industry="manufacturing",
)


fake_result = LLMResearchResult(
    summary="Test result",
    findings=[
        LLMFinding(
            title="Fake finding",
            description="Testing validation.",
            source_ids=["S99"],
        )
    ],
    opportunities=[],
    risks=[],
    source_ids=["S99"],
    confidence=LLMEvidenceConfidence(
        level="Low",
        explanation="Test only.",
    ),
)


validation = validate_citations(
    result=fake_result,
    evidence_items=evidence,
)


print(
    "Validation passed:",
    validation.is_valid
)


for error in validation.errors:
    print(
        "-",
        error
    )