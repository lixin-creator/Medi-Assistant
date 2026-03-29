"""
MediAssistant 鈥?tools/serper_search.py
Serper web search tool singleton.
"""

from __future__ import annotations

from typing import Any, Dict, List

import httpx

from app.core.config import SERPER_API_KEY
from app.core.logging_config import logger

_serper_search = None


class SerperSearchTool:
    """Small Serper client with a LangChain-like invoke interface."""

    def __init__(self, api_key: str, max_results: int = 3):
        self.api_key = api_key
        self.max_results = max_results

    def invoke(self, query: str) -> List[Dict[str, Any]]:
        response = httpx.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
            json={"q": query, "num": self.max_results},
            timeout=20.0,
        )
        response.raise_for_status()

        payload = response.json()
        organic_results = payload.get("organic", []) or []

        return [
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "content": item.get("snippet", ""),
            }
            for item in organic_results[: self.max_results]
        ]


def get_serper_search():
    """Return a cached Serper search tool, or None if API key is missing."""
    global _serper_search
    if _serper_search is None:
        if not SERPER_API_KEY:
            logger.warning("SERPER_API_KEY not found in environment variables")
            return None

        _serper_search = SerperSearchTool(api_key=SERPER_API_KEY, max_results=3)
        logger.info("Serper search tool initialized")
    return _serper_search

