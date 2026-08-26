from typing import List
from uuid import uuid4

from app.models.evidence import EvidenceItem
from app.models.research import (
    EvidenceConfidence,
    Finding,
    Opportunity,
    ResearchRequest,
    ResearchResponse,
    Risk,
    SourceReference,
)
from app.services.llm_service import (
    generate_research_result,
)
from app.services.retrieval_service import (
    retrieve_evidence,
)
from app.services.validation_service import (
    validate_citations,
)
from app.repositories.research_repository import (
    save_research,
)
from app.models.exceptions import ValidationError
from app.services.evidence_service import (
    assess_evidence,
)
import logging
import time

logger = logging.getLogger(
    __name__
)

def run_research(
    request: ResearchRequest,
) -> ResearchResponse:

    research_id = str(uuid4())
    start_time = time.perf_counter()

    logger.info(
    "Research started | "
    "research_id=%s | "
    "query=%s | "
    "industry=%s",
    research_id,
    request.query,
    request.industry,
)

    retrieval_start = time.perf_counter()

    evidence = retrieve_evidence(
        query=request.query,
        top_k=3,
        industry=request.industry,
    )

    retrieval_latency = (
        time.perf_counter()
        - retrieval_start
    )

    logger.info(
        "Retrieval completed | "
        "research_id=%s | "
        "chunks=%s | "
        "latency_ms=%.2f",
        research_id,
        len(evidence),
        retrieval_latency * 1000,
    )

    for item in evidence:
        logger.info(
            "Evidence retrieved | "
            "research_id=%s | "
            "citation_id=%s | "
            "chunk_id=%s | "
            "distance=%.4f",
            research_id,
            item.citation_id,
            item.chunk_id,
            item.distance,
        )

    evidence_assessment = (
    assess_evidence(
        evidence
    )
    
)
    logger.info(
    "Evidence assessed | "
    "research_id=%s | "
    "level=%s | "
    "average_distance=%s | "
    "evidence_count=%s | "
    "unique_sources=%s",
    research_id,
    evidence_assessment.level,
    evidence_assessment.average_distance,
    evidence_assessment.evidence_count,
    evidence_assessment.unique_source_count,
)
    
    if (
        not evidence
        or evidence_assessment.level == "Low"
    ):
        response = ResearchResponse(
            research_id=research_id,
            query=request.query,
            summary=(
                "Insufficient evidence was found "
                "to answer this question reliably."
            ),
            findings=[],
            opportunities=[],
            risks=[],
            sources=[],
            confidence=EvidenceConfidence(
                level="Low",
                explanation=(
                    evidence_assessment.explanation
                ),
            ),
        )

        save_research(
            research_id=response.research_id,
            query=response.query,
            summary=response.summary,
            confidence_level=(
                response.confidence.level
            ),
            confidence_explanation=(
                response.confidence.explanation
            ),
        )

        total_latency = (
            time.perf_counter()
            - start_time
        )

        logger.warning(
            "Research stopped due to weak evidence | "
            "research_id=%s | "
            "total_latency_ms=%.2f",
            research_id,
            total_latency * 1000,
        )

        return response

    llm_start = time.perf_counter()

    llm_result = generate_research_result(
        query=request.query,
        evidence_items=evidence,
    )

    llm_latency = (
        time.perf_counter()
        - llm_start
    )

    logger.info(
        "LLM generation completed | "
        "research_id=%s | "
        "latency_ms=%.2f",
        research_id,
        llm_latency * 1000,
    )

    validation = validate_citations(
        result=llm_result,
        evidence_items=evidence,
    )

    logger.info(
    "Citation validation completed | "
    "research_id=%s | "
    "valid=%s | "
    "errors=%s",
    research_id,
    validation.is_valid,
    len(validation.errors),
)

    if not validation.is_valid:

        logger.warning(
            "Regenerating due to "
            "citation validation failure | "
            "research_id=%s",
            research_id,
        )

        llm_result = generate_research_result(
            query=request.query,
            evidence_items=evidence,
        )

        validation = validate_citations(
            result=llm_result,
            evidence_items=evidence,
        )


    if not validation.is_valid:
        raise ValidationError(
            "Generated research result failed "
            "citation validation after retry: "
            + "; ".join(validation.errors)
        )

    sources = build_source_references(
        evidence
    )
    response = ResearchResponse(
        research_id=research_id,
        query=request.query,
        summary=llm_result.summary,
        findings=[
            Finding(
                title=item.title,
                description=item.description,
                source_ids=item.source_ids,
            )
            for item in llm_result.findings
        ],
        opportunities=[
            Opportunity(
                title=item.title,
                description=item.description,
                expected_value=item.expected_value,
                difficulty=item.difficulty,
                source_ids=item.source_ids,
            )
            for item in llm_result.opportunities
        ],
        risks=[
            Risk(
                title=item.title,
                description=item.description,
                source_ids=item.source_ids,
            )
            for item in llm_result.risks
        ],
        sources=sources,
        confidence=EvidenceConfidence(
        level=evidence_assessment.level,
        explanation=(
            evidence_assessment.explanation
            + " "
            + llm_result.confidence.explanation
        ),
    ),
    )


    save_research(
        research_id=response.research_id,
        query=response.query,
        summary=response.summary,
        confidence_level=response.confidence.level,
        confidence_explanation=response.confidence.explanation,
    )

    total_latency = (
        time.perf_counter()
        - start_time
    )

    logger.info(
        "Research completed | "
        "research_id=%s | "
        "total_latency_ms=%.2f | "
        "confidence=%s",
        research_id,
        total_latency * 1000,
        response.confidence.level,
    )

    return response


def build_source_references(
    evidence_items: List[EvidenceItem],
) -> List[SourceReference]:

    sources = []

    for item in evidence_items:
        sources.append(
            SourceReference(
                source_id=item.citation_id,
                source_name=item.source_name,
                evidence_text=item.content,
            )
        )

    return sources