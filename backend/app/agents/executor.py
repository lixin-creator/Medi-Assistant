"""
MediAssistant 鈥?agents/executor.py
ExecutorAgent: synthesizes the final response using the LLM and gathered context.
"""

from app.core.logging_config import logger
from app.core.state import AgentState
from app.tools.llm_client import get_llm


def _get_language_instruction(language: str) -> str:
    return "Respond in Chinese." if language == "zh" else "Respond in English."


def _build_document_fallback_answer(state: AgentState) -> str:
    """Return a deterministic answer from retrieved docs when LLM is unavailable."""
    snippets = [
        doc.page_content.strip()
        for doc in state.get("documents", [])[:2]
        if getattr(doc, "page_content", "").strip()
    ]
    context = " ".join(snippets)
    if not context:
        return (
            "Medical AI service temporarily unavailable. "
            "Please consult a healthcare professional."
        )
    trimmed = context[:280].strip()
    suffix = "..." if len(context) > 280 else ""
    return (
        f"Based on available medical references: {trimmed}{suffix} "
        "Please consult a healthcare professional for personalized advice."
    )


def ExecutorAgent(state: AgentState) -> AgentState:
    """Synthesize the final patient response from retrieved documents or LLM knowledge."""
    llm = get_llm()
    question = state["question"]
    source_info = state.get("source", "Unknown")

    # Build recent conversation context
    history_context = ""
    for item in state.get("conversation_history", [])[-3:]:
        if item.get("role") == "user":
            history_context += f"Patient: {item.get('content', '')}\n"
        elif item.get("role") == "assistant":
            history_context += f"Doctor: {item.get('content', '')}\n"

    language_instruction = _get_language_instruction(state.get("language", "en"))

    if state.get("documents") and len(state["documents"]) > 0 and not llm:
        answer = _build_document_fallback_answer(state)
        source_info = "Local Knowledge Fallback"

    elif not llm:
        answer = (
            "Medical AI service temporarily unavailable. "
            "Please consult a healthcare professional."
        )
        source_info = "System Message"

    elif state.get("documents") and len(state["documents"]) > 0:
        content = "\n\n".join(
            [doc.page_content[:1000] for doc in state["documents"][:3]]
        )
        prompt = (
            "You are an experienced medical doctor providing helpful consultation.\n\n"
            f"{language_instruction}\n"
            f"Previous Conversation:\n{history_context}\n"
            f"Patient's Current Question:\n{question}\n\n"
            f"Medical Information:\n{content}\n\n"
            "Provide a clear, caring response in 2-4 sentences. Be professional and reassuring."
        )
        try:
            response = llm.invoke(prompt)
            answer = (
                response.content.strip()
                if hasattr(response, "content")
                else str(response).strip()
            )
            logger.info("Executor: Generated response from documents")
        except Exception as e:
            logger.error("Executor: LLM generation failed: %s", str(e))
            answer = (
                "I understand your concern about your symptoms. For accurate medical advice, "
                "please consult with a healthcare professional who can properly evaluate your condition."
            )
            source_info = "System Message"

    elif state.get("llm_success") and state.get("generation"):
        answer = state["generation"]
        logger.info("Executor: Using pre-generated LLM response")

    else:
        answer = (
            "I understand your concern about your symptoms. For accurate medical advice, "
            "please consult with a healthcare professional who can properly evaluate your condition."
        )
        source_info = "System Message"

    state["generation"] = answer
    state["source"] = source_info
    state["conversation_history"].append({"role": "user", "content": question})
    state["conversation_history"].append(
        {"role": "assistant", "content": answer, "source": source_info}
    )
    return state
