import json
import logging
from typing import List

from groq import Groq

from app.config.settings import settings
from app.models.evidence import EvidenceItem
from app.models.evidence_comparison import (
    EvidenceComparisonResult,
)
from app.prompts.evidence_comparison_prompt import (
    build_evidence_comparison_prompt,
)


logger = logging.getLogger(__name__)


def compare_evidence(
    evidence_items: List[EvidenceItem],
) -> EvidenceComparisonResult:

    if len(evidence_items) < 2:
        return EvidenceComparisonResult(
            comparisons=[]
        )

    client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    prompt = build_evidence_comparison_prompt(
        evidence_items
    )

    max_attempts = 2

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        try:
            logger.info(
                "Evidence comparison LLM call | "
                "attempt=%s",
                attempt,
            )

            response = (
                client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=0,
                )
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if not content:
                raise ValueError(
                    "Empty comparison response."
                )

            content = content.strip()

            if content.startswith("```json"):
                content = content[7:]

            elif content.startswith("```"):
                content = content[3:]

            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

            parsed = json.loads(
                content
            )

            result = EvidenceComparisonResult(
                **parsed
            )

            return validate_comparison_sources(
                result=result,
                evidence_items=evidence_items,
            )

        except (
            json.JSONDecodeError,
            ValueError,
        ) as exc:

            logger.warning(
                "Evidence comparison parsing failed | "
                "attempt=%s | error=%s",
                attempt,
                exc,
            )

            if attempt == max_attempts:
                return EvidenceComparisonResult(
                    comparisons=[]
                )

        except Exception as exc:

            logger.warning(
                "Evidence comparison failed | "
                "attempt=%s | error=%s",
                attempt,
                exc,
            )

            if attempt == max_attempts:
                return EvidenceComparisonResult(
                    comparisons=[]
                )

    return EvidenceComparisonResult(
        comparisons=[]
    )


def validate_comparison_sources(
    result: EvidenceComparisonResult,
    evidence_items: List[EvidenceItem],
) -> EvidenceComparisonResult:

    valid_ids = {
        item.citation_id
        for item in evidence_items
    }

    valid_comparisons = []

    for comparison in result.comparisons:

        source_ids = [
            source_id
            for source_id
            in comparison.supporting_sources
            if source_id in valid_ids
        ]

        if len(source_ids) < 2:
            continue

        comparison.supporting_sources = (
            source_ids
        )

        valid_comparisons.append(
            comparison
        )

    return EvidenceComparisonResult(
        comparisons=valid_comparisons
    )