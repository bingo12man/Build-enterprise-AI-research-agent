import logging
import os
from typing import List

from tavily import TavilyClient

from app.models.web_source import WebSource
from app.config.settings import settings
from app.models.evidence import EvidenceItem
logger = logging.getLogger(__name__)


def search_web(
    query: str,
    max_results: int = 5,
) -> List[WebSource]:

    if not query or not query.strip():
        return []

    api_key = settings.TAVILY_API_KEY
    if not api_key:
        logger.warning(
            "TAVILY_API_KEY is not configured."
        )
        return []

    try:
        client = TavilyClient(
            api_key=api_key
        )

        response = client.search(
            query=query.strip(),
            max_results=max_results,
            search_depth="basic",
        )

        sources: List[WebSource] = []

        for result in response.get(
            "results",
            [],
        ):
            title = result.get("title")
            url = result.get("url")
            content = result.get("content")

            if not title or not url or not content:
                continue

            sources.append(
                WebSource(
                    title=title,
                    url=url,
                    content=content,
                    source_type="web",
                )
            )

        logger.info(
            "External web research completed: "
            "query=%s results=%s",
            query,
            len(sources),
        )

        return sources

    except Exception as exc:
        logger.warning(
            "External web research failed: %s",
            exc,
        )

        return []

def convert_web_sources_to_evidence(
    sources: List[WebSource],
    start_index: int = 1,
) -> List[EvidenceItem]:

    evidence_items: List[EvidenceItem] = []

    for index, source in enumerate(
        sources,
        start=start_index,
    ):
        evidence_items.append(
            EvidenceItem(
                citation_id=f"S{index}",
                content=source.content,
                source_id=source.url,
                source_name=source.title,
                source_type="web",
                source_url=source.url,
                chunk_id=None,
                distance=None,
            )
        )

    return evidence_items