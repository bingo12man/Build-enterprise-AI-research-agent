import json
import logging
from typing import List

from groq import Groq

from app.config.settings import settings
from app.models.contradiction import (
    ContradictionResult,
)
from app.models.evidence import (
    EvidenceItem,
)
from app.prompts.contradiction_prompt import (
    build_contradiction_prompt,
)


logger = logging.getLogger(__name__)


def detect_contradictions(
    evidence_items: List[EvidenceItem],
) -> ContradictionResult:

    if len(evidence_items) < 2:
        return ContradictionResult(
            contradictions=[]
        )

    client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    prompt = build_contradiction_prompt(
        evidence_items
    )

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        if not content:
            return ContradictionResult(
                contradictions=[]
            )

        content = content.strip()

        if content.startswith("```"):
            content = (
                content
                .replace(
                    "```json",
                    "",
                )
                .replace(
                    "```",
                    "",
                )
                .strip()
            )

        parsed = json.loads(
            content
        )

        result = ContradictionResult(
            **parsed
        )

        return validate_contradictions(
            result=result,
            evidence_items=evidence_items,
        )

    except Exception as exc:

        logger.warning(
            "Contradiction detection failed: %s",
            exc,
        )

        return ContradictionResult(
            contradictions=[]
        )


def validate_contradictions(
    result: ContradictionResult,
    evidence_items: List[EvidenceItem],
) -> ContradictionResult:

    valid_ids = {
        item.citation_id
        for item in evidence_items
    }

    valid_contradictions = []

    for contradiction in result.contradictions:

        source_ids = [
            source_id
            for source_id
            in contradiction.source_ids
            if source_id in valid_ids
        ]

        source_ids = list(
            dict.fromkeys(
                source_ids
            )
        )

        if len(source_ids) < 2:
            continue

        contradiction.source_ids = (
            source_ids
        )

        valid_contradictions.append(
            contradiction
        )

    return ContradictionResult(
        contradictions=valid_contradictions
    )