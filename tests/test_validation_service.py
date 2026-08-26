from app.models.evidence import (
    EvidenceItem,
)
from app.models.llm import (
    LLMEvidenceConfidence,
    LLMFinding,
    LLMOpportunity,
    LLMResearchResult,
    LLMRisk,
)
from app.services.validation_service import (
    validate_citations,
)


def make_evidence():

    return [
        EvidenceItem(
            citation_id="S1",
            chunk_id="chunk-1",
            content="Predictive maintenance evidence.",
            source_id="source-1",
            source_name="manufacturing_ai.txt",
            distance=1.0,
            industry="manufacturing",
        ),
        EvidenceItem(
            citation_id="S2",
            chunk_id="chunk-2",
            content="Computer vision evidence.",
            source_id="source-1",
            source_name="manufacturing_ai.txt",
            distance=1.1,
            industry="manufacturing",
        ),
    ]


def make_valid_result():

    return LLMResearchResult(
        summary="AI can improve manufacturing.",
        findings=[
            LLMFinding(
                title="Predictive Maintenance",
                description=(
                    "AI can identify equipment "
                    "failure patterns."
                ),
                source_ids=["S1"],
            )
        ],
        opportunities=[
            LLMOpportunity(
                title="Reduce Downtime",
                description=(
                    "Use predictive maintenance."
                ),
                expected_value="High",
                difficulty="Medium",
                source_ids=["S1"],
            )
        ],
        risks=[
            LLMRisk(
                title="Data Quality",
                description=(
                    "Poor data can reduce "
                    "prediction quality."
                ),
                source_ids=["S1"],
            )
        ],
        source_ids=[
            "S1"
        ],
        confidence=LLMEvidenceConfidence(
            level="High",
            explanation=(
                "Evidence directly supports "
                "the response."
            ),
        ),
    )


def test_valid_citations_pass():

    result = make_valid_result()

    validation = (
        validate_citations(
            result,
            make_evidence(),
        )
    )

    assert validation.is_valid is True
    assert validation.errors == []


def test_fake_citation_fails():

    result = make_valid_result()

    result.findings[0].source_ids = [
        "S99"
    ]

    validation = (
        validate_citations(
            result,
            make_evidence(),
        )
    )

    assert validation.is_valid is False
    assert len(validation.errors) > 0


def test_missing_claim_citation_fails():

    result = make_valid_result()

    result.risks[0].source_ids = []

    validation = (
        validate_citations(
            result,
            make_evidence(),
        )
    )

    assert validation.is_valid is False