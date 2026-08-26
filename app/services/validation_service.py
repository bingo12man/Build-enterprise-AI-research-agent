from typing import List

from app.models.evidence import EvidenceItem
from app.models.llm import LLMResearchResult
from app.models.validation import ValidationResult


def validate_citations(
    result: LLMResearchResult,
    evidence_items: List[EvidenceItem],
) -> ValidationResult:

    errors = []

    valid_citation_ids = {
        item.citation_id
        for item in evidence_items
    }

    generated_citation_ids = set()

    for finding in result.findings:
        generated_citation_ids.update(
            finding.source_ids
        )

        if not finding.source_ids:
            errors.append(
                f"Finding '{finding.title}' "
                "has no supporting citations."
            )

    for opportunity in result.opportunities:
        generated_citation_ids.update(
            opportunity.source_ids
        )

        if not opportunity.source_ids:
            errors.append(
                f"Opportunity "
                f"'{opportunity.title}' "
                "has no supporting citations."
            )

    for risk in result.risks:
        generated_citation_ids.update(
            risk.source_ids
        )

        if not risk.source_ids:
            errors.append(
                f"Risk '{risk.title}' "
                "has no supporting citations."
            )

    generated_citation_ids.update(
        result.source_ids
    )

    invalid_citations = (
        generated_citation_ids
        - valid_citation_ids
    )

    for citation_id in sorted(
        invalid_citations
    ):
        errors.append(
            f"Invalid citation ID: "
            f"{citation_id}"
        )

    claim_citation_ids = set()

    for finding in result.findings:
        claim_citation_ids.update(
            finding.source_ids
        )

    for opportunity in result.opportunities:
        claim_citation_ids.update(
            opportunity.source_ids
        )

    for risk in result.risks:
        claim_citation_ids.update(
            risk.source_ids
        )

    overall_source_ids = set(
        result.source_ids
    )

    missing_from_overall = (
        claim_citation_ids
        - overall_source_ids
    )

    for citation_id in sorted(
        missing_from_overall
    ):
        errors.append(
            f"Citation {citation_id} "
            "is used in a claim but missing "
            "from the overall source list."
        )

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
    )