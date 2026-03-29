"""
MediAssistant 鈥?tools/vector_store.py
Vector store management: embeddings, creation, loading, and retriever factory.
"""

import os
import sys
from typing import List, Optional

from langchain_core.documents import Document

from app.core.config import VECTOR_STORE_DIR
from app.core.logging_config import logger

_embeddings = None
_vectorstore = None


def _get_vectorstore_backend() -> str:
    """Return the configured vector store backend."""
    backend = os.getenv("VECTOR_STORE_BACKEND")
    if backend:
        return backend.lower()
    return "sklearn" if sys.platform.startswith("win") else "chroma"


def _get_sklearn_persist_path(persist_dir: str) -> str:
    """Return the persist file path for the sklearn vector store."""
    return os.path.join(persist_dir, "vector_store.json")


def _get_vectorstore_count(store) -> int:
    """Return the document count for supported vector store implementations."""
    collection = getattr(store, "_collection", None)
    if collection is not None:
        return collection.count()

    ids = getattr(store, "_ids", None)
    if ids is not None:
        return len(ids)

    return 0


def get_embeddings():
    """Return a cached HuggingFace sentence-transformer embeddings instance."""
    global _embeddings
    if _embeddings is None:
        from langchain_huggingface.embeddings import HuggingFaceEmbeddings

        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("Embeddings model loaded (all-MiniLM-L6-v2)")
    return _embeddings


def get_or_create_vectorstore(
    documents: Optional[List[Document]] = None,
    persist_dir: str = VECTOR_STORE_DIR,
):
    """Load an existing vector store or create a new one from documents."""
    global _vectorstore

    if _vectorstore is not None:
        return _vectorstore

    embeddings = get_embeddings()
    backend = _get_vectorstore_backend()

    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)

    if backend == "sklearn":
        from langchain_community.vectorstores.sklearn import SKLearnVectorStore

        persist_path = _get_sklearn_persist_path(persist_dir)
        store_exists = os.path.isfile(persist_path)

        if store_exists:
            logger.info("Loading existing sklearn vector store from %s", persist_path)
            _vectorstore = SKLearnVectorStore(
                embedding=embeddings,
                persist_path=persist_path,
                serializer="json",
            )
            count = _get_vectorstore_count(_vectorstore)
            if count == 0:
                logger.warning("Vector store is empty 鈥?needs to be recreated")
                _vectorstore = None
                return None
            logger.info("Loaded %d documents from vector store", count)
        elif documents:
            logger.info(
                "Creating new sklearn vector store with %d documents", len(documents)
            )
            _vectorstore = SKLearnVectorStore.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_path=persist_path,
                serializer="json",
            )
            _vectorstore.persist()
        else:
            logger.warning("No existing vector store and no documents provided")
            return None
    else:
        from langchain_community.vectorstores import Chroma

        db_files_exist = any(
            f.endswith(".sqlite3") or f == "chroma.sqlite3" or f.startswith("index")
            for f in os.listdir(persist_dir)
        ) if os.path.exists(persist_dir) else False

        if db_files_exist:
            logger.info("Loading existing Chroma vector store from %s", persist_dir)
            _vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=embeddings,
                collection_metadata={"hnsw:space": "cosine"},
            )
            count = _get_vectorstore_count(_vectorstore)
            if count == 0:
                logger.warning("Vector store is empty 鈥?needs to be recreated")
                _vectorstore = None
                return None
            logger.info("Loaded %d documents from vector store", count)
        elif documents:
            logger.info("Creating new Chroma vector store with %d documents", len(documents))
            _vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=persist_dir,
                collection_metadata={"hnsw:space": "cosine"},
            )
            _vectorstore.persist()
        else:
            logger.warning("No existing vector store and no documents provided")
            return None

    return _vectorstore


def get_retriever(k: int = 3):
    """Return a retriever from the vector store, or None if unavailable."""
    vs = get_or_create_vectorstore()
    if vs:
        return vs.as_retriever(search_kwargs={"k": k})
    return None

