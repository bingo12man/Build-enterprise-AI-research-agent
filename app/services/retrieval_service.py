from typing import List, Optional

from app.models.evidence import EvidenceItem
from app.services.embedding_service import embed_text
from app.services.vector_store_service import search_chunks
from app.models.exceptions import RetrievalError
from app.config.settings import settings

def retrieve_evidence(
    query: str,
    top_k: int = settings.RETRIEVAL_TOP_K,
    industry: Optional[str] = None,
    max_distance: Optional[float] = None,
) -> List[EvidenceItem]:

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    try:
        query_embedding = embed_text(
            query
        )

        results = search_chunks(
            query_embedding=query_embedding,
            top_k=top_k,
            industry=industry,
        )

    except Exception as error:
        raise RetrievalError(
            "Evidence retrieval failed."
        ) from error

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    evidence_items = []

    for (
        chunk_id,
        content,
        metadata,
        distance,
    ) in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):

        if (
            max_distance is not None
            and distance > max_distance
        ):
            continue

        citation_id = (
            f"S{len(evidence_items) + 1}"
        )

        evidence_items.append(
            EvidenceItem(
                citation_id=citation_id,
                chunk_id=chunk_id,
                content=content,
                source_id=metadata["source_id"],
                source_name=metadata["source_name"],
                distance=float(distance),
                industry=metadata.get("industry"),
                document_type=metadata.get(
                    "document_type"
                ),
            )
        )

    return evidence_items