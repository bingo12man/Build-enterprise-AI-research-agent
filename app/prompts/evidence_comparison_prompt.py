from typing import List

from app.models.evidence import EvidenceItem


def build_evidence_comparison_prompt(
    evidence_items: List[EvidenceItem],
) -> str:

    evidence_blocks = []

    for item in evidence_items:
        evidence_blocks.append(
            (
                f"CITATION_ID: {item.citation_id}\n"
                f"SOURCE_TYPE: {item.source_type}\n"
                f"SOURCE_NAME: {item.source_name}\n"
                f"CONTENT:\n{item.content}"
            )
        )

    evidence_text = "\n\n---\n\n".join(
        evidence_blocks
    )

    return f"""
You are comparing research evidence from multiple sources.

Your task is to identify important topics that are supported
by two or more evidence sources.

Rules:
1. Use only the evidence provided below.
2. Do not invent facts.
3. Do not invent citation IDs.
4. supporting_sources must contain only citation IDs
   that directly support the comparison.
5. Prefer comparisons that involve different sources.
6. When possible, compare internal evidence with external
   web evidence.
7. If sources add different perspectives to the same topic,
   explain that clearly.
8. Do not identify contradictions yet.
   Contradiction detection is handled separately.

Return JSON only using this structure:

{{
    "comparisons": [
        {{
            "topic": "short topic",
            "supporting_sources": ["S1", "S4"],
            "summary": "what these sources collectively show"
        }}
    ]
}}

If there are no meaningful comparisons, return:

{{
    "comparisons": []
}}

EVIDENCE:

{evidence_text}
""".strip()