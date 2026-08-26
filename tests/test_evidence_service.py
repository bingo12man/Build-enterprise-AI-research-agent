from app.models.evidence import (
    EvidenceItem,
)
from app.services.evidence_service import (
    assess_evidence,
)


def make_evidence(
    citation_id: str,
    distance: float,
) -> EvidenceItem:

    return EvidenceItem(
        citation_id=citation_id,
        chunk_id=f"chunk-{citation_id}",
        content="Manufacturing AI evidence.",
        source_id="source-1",
        source_name="manufacturing_ai.txt",
        distance=distance,
        industry="manufacturing",
    )


def test_high_quality_evidence():

    evidence = [
        make_evidence(
            "S1",
            1.00,
        ),
        make_evidence(
            "S2",
            1.20,
        ),
        make_evidence(
            "S3",
            1.30,
        ),
    ]

    result = assess_evidence(
        evidence
    )

    assert result.level == "High"
    assert result.evidence_count == 3


def test_low_quality_evidence():

    evidence = [
        make_evidence(
            "S1",
            1.85,
        ),
        make_evidence(
            "S2",
            1.95,
        ),
        make_evidence(
            "S3",
            2.00,
        ),
    ]

    result = assess_evidence(
        evidence
    )

    assert result.level == "Low"


def test_empty_evidence_is_low():

    result = assess_evidence(
        []
    )

    assert result.level == "Low"
    assert result.evidence_count == 0