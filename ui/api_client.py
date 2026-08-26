import os
from typing import Any, Dict, List, Optional

import requests


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

def run_research(
    query: str,
    industry: Optional[str] = None,
) -> Dict[str, Any]:

    payload = {
        "query": query,
        "industry": industry,
    }

    response = requests.post(
        f"{API_BASE_URL}/research",
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def get_history(
    limit: int = 10,
) -> List[Dict[str, Any]]:

    response = requests.get(
        f"{API_BASE_URL}/history",
        params={
            "limit": limit,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_history_item(
    research_id: str,
) -> Dict[str, Any]:

    response = requests.get(
        f"{API_BASE_URL}/history/{research_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()