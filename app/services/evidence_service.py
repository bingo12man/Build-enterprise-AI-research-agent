from typing import List

from app.models.evidence import (
    EvidenceAssessment,
    EvidenceItem,
)


from app.config.settings import settings


HIGH_DISTANCE_THRESHOLD = (
    settings.HIGH_DISTANCE_THRESHOLD
)

MEDIUM_DISTANCE_THRESHOLD = (
    settings.MEDIUM_DISTANCE_THRESHOLD
)


def assess_evidence(
    evidence_items: List[EvidenceItem],
) -> EvidenceAssessment:

    if not evidence_items:
        return EvidenceAssessment(
            level="Low",
            explanation=(
                "No relevant evidence was retrieved."
            ),
            average_distance=None,
            evidence_count=0,
            unique_source_count=0,
        )

    distances = [
        item.distance
        for item in evidence_items
    ]

    average_distance = (
        sum(distances) / len(distances)
    )

    best_distance = min(
        distances
    )

    unique_source_ids = {
        item.source_id
        for item in evidence_items
    }

    unique_source_count = len(
        unique_source_ids
    )

    if (
        best_distance <= HIGH_DISTANCE_THRESHOLD
        and average_distance
        <= MEDIUM_DISTANCE_THRESHOLD
    ):
        level = "High"

        explanation = (
            "At least one retrieved chunk has "
            "strong semantic similarity and the "
            "overall evidence is relevant."
        )

    elif (
        best_distance
        <= MEDIUM_DISTANCE_THRESHOLD
    ):
        level = "Medium"

        explanation = (
            "Retrieved evidence has moderate "
            "semantic similarity to the query."
        )

    else:
        level = "Low"

        explanation = (
            "Retrieved evidence has weak "
            "semantic similarity to the query."
        )

    return EvidenceAssessment(
        level=level,
        explanation=explanation,
        average_distance=average_distance,
        evidence_count=len(
            evidence_items
        ),
        unique_source_count=(
            unique_source_count
        ),
    )