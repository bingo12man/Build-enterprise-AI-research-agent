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

    # Only internal Chroma evidence has
    # a semantic distance score.
    distances = [
        item.distance
        for item in evidence_items
        if item.distance is not None
    ]

    unique_source_ids = {
        item.source_id
        for item in evidence_items
    }

    unique_source_count = len(
        unique_source_ids
    )

    web_evidence_count = len(
        [
            item
            for item in evidence_items
            if item.source_type == "web"
        ]
    )

    # Case 1:
    # We have internal vector evidence.
    if distances:

        average_distance = (
            sum(distances)
            / len(distances)
        )

        best_distance = min(
            distances
        )

        if (
            best_distance
            <= HIGH_DISTANCE_THRESHOLD
            and average_distance
            <= MEDIUM_DISTANCE_THRESHOLD
        ):
            level = "High"

            explanation = (
                "Strong semantic evidence was "
                "retrieved from the internal "
                "knowledge base."
            )

            if web_evidence_count > 0:
                explanation += (
                    " Additional external web "
                    "sources were also retrieved "
                    "for comparison."
                )

        elif (
            best_distance
            <= MEDIUM_DISTANCE_THRESHOLD
        ):
            level = "Medium"

            explanation = (
                "Internal evidence has moderate "
                "semantic similarity to the query."
            )

            if web_evidence_count > 0:
                explanation += (
                    " External web evidence was "
                    "also retrieved."
                )

        else:
            level = "Low"

            explanation = (
                "Internal evidence has weak "
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

    # Case 2:
    # No internal vector evidence,
    # but external web research exists.
    if web_evidence_count >= 2:

        return EvidenceAssessment(
            level="Medium",
            explanation=(
                "No strong internal knowledge-base "
                "evidence was available, but multiple "
                "external web sources were retrieved. "
                "The result should therefore be treated "
                "with moderate confidence."
            ),
            average_distance=None,
            evidence_count=len(
                evidence_items
            ),
            unique_source_count=(
                unique_source_count
            ),
        )

    return EvidenceAssessment(
        level="Low",
        explanation=(
            "Insufficient reliable evidence was "
            "retrieved to support the research query."
        ),
        average_distance=None,
        evidence_count=len(
            evidence_items
        ),
        unique_source_count=(
            unique_source_count
        ),
    )