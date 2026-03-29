"""
MediAssistant 鈥?agents/serper.py
SerperAgent: searches the web via Serper for current medical information.
"""

from langchain_core.documents import Document

from app.core.logging_config import logger
from app.core.state import AgentState
from app.tools.serper_search import get_serper_search


def SerperAgent(state: AgentState) -> AgentState:
    """Search the web via Serper for current medical research and news."""
    serper = get_serper_search()
    if not serper:
        state["documents"] = []
        state["serper_success"] = False
        state["serper_attempted"] = True
        return state

    search_query = f"{state['question']} medical health treatment symptoms"
    try:
        results = serper.invoke(search_query)
    except Exception as error:
        logger.error("Serper: Search failed: %s", str(error))
        results = []

    valid_results = [
        result
        for result in (results or [])
        if isinstance(result, dict)
        and result.get("content")
        and len(result["content"].strip()) > 50
    ]

    if valid_results:
        state["documents"] = [
            Document(
                page_content=result["content"],
                metadata={
                    "url": result.get("url", ""),
                    "title": result.get("title", ""),
                },
            )
            for result in valid_results
        ]
        state["serper_success"] = True
        state["source"] = "Web Search"
        logger.info("Serper: Found %d results", len(valid_results))
    else:
        state["documents"] = []
        state["serper_success"] = False
        logger.info("Serper: No valid results")

    state["serper_attempted"] = True
    return state

