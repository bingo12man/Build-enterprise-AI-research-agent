from typing import List

from app.models.evidence import EvidenceItem


def build_contradiction_prompt(
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
You are analyzing research evidence from multiple sources.

Your task is to identify genuine contradictions between sources.

A contradiction exists only when two or more sources make
incompatible claims about the same topic.

Rules:
1. Use only the evidence provided below.
2. Do not invent facts.
3. Do not invent citation IDs.
4. Do not label different levels of detail as contradictions.
5. Do not label different examples as contradictions.
6. Do not label complementary claims as contradictions.
7. Only report a contradiction when the claims cannot both
   reasonably be true at the same time.
8. Each contradiction must reference at least two citation IDs.
9. If no genuine contradiction exists, return an empty list.

Return JSON only using this structure:

{{
    "contradictions": [
        {{
            "topic": "short topic",
            "source_ids": ["S1", "S4"],
            "explanation": "Explain exactly how the claims conflict."
        }}
    ]
}}

If there are no contradictions, return:

{{
    "contradictions": []
}}

EVIDENCE:

{evidence_text}
""".strip()