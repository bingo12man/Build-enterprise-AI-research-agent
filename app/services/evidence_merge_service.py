from typing import List

from app.models.evidence import EvidenceItem


def merge_evidence(
    local_evidence: List[EvidenceItem],
    web_evidence: List[EvidenceItem],
) -> List[EvidenceItem]:

    combined = local_evidence + web_evidence

    merged: List[EvidenceItem] = []

    for index, item in enumerate(
        combined,
        start=1,
    ):
        updated_item = item.model_copy(
            update={
                "citation_id": f"S{index}"
            }
        )

        merged.append(updated_item)

    return merged