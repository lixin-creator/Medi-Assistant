"""
MediAssistant Backend 鈥?main.py
FastAPI application entry point: app setup, lifespan, and router registration.

Module layout:
  core/               鈥?config, logging, state, workflow
  agents/             鈥?8 individual LangGraph agent nodes
  tools/              鈥?LLM client, vector store, PDF loader, search tools
  db/                 鈥?SQLAlchemy session factory
  models/             鈥?ORM models
  schemas/            鈥?Pydantic request/response schemas
  services/           鈥?DatabaseService, ChatService
  api/v1/endpoints/   鈥?health, chat, session route handlers
  api/v1/api.py       鈥?router aggregator
  main.py             鈥?FastAPI app + lifespan  鈫?you are here
"""

import os
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.api import api_router
from app.core.config import CHAT_DB_PATH, PDF_PATH, VECTOR_STORE_DIR
from app.core.logging_config import logger
from app.services.chat_service import chat_service
from app.services.database_service import db_service
from app.tools.pdf_loader import process_pdf
from app.tools.vector_store import get_or_create_vectorstore


# 鈹€鈹€ Lifespan 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info("Initializing MediAssistant System...")

    db_service.init_db()
    logger.info("Database initialized at %s", CHAT_DB_PATH)

    if os.path.exists(PDF_PATH):
        logger.info("Processing PDF: %s", PDF_PATH)
        documents = process_pdf(PDF_PATH)
        get_or_create_vectorstore(documents)
        logger.info("Vector store ready at %s", VECTOR_STORE_DIR)
    else:
        logger.warning("PDF not found at %s 鈥?vector store skipped", PDF_PATH)

    chat_service.initialize_workflow()
    logger.info("MediAssistant System Ready!")

    yield

    logger.info("Shutting down MediAssistant...")


# 鈹€鈹€ FastAPI App 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
app = FastAPI(
    title="MediAssistant API",
    description="AI-powered medical consultation system 鈥?Deep Modular + Agentic Architecture",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

# Register all API routes
app.include_router(api_router)


# 鈹€鈹€ Entry Point 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

