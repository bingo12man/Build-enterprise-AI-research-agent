from typing import List

import chromadb

from app.models.document import DocumentChunk
from app.config.settings import settings


PERSIST_DIRECTORY = "data/chroma_db"
COLLECTION_NAME = "enterprise_documents"


_client = chromadb.PersistentClient(
    path=PERSIST_DIRECTORY
)


_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME
)


def add_chunks(
    chunks: List[DocumentChunk],
    embeddings: List[List[float]],
) -> None:

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    if not chunks:
        return

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(
            chunk.chunk_id
        )

        documents.append(
            chunk.content
        )

        metadata = {
            "source_id": chunk.metadata.source_id,
            "source_name": chunk.metadata.source_name,
        }

        if chunk.metadata.industry is not None:
            metadata["industry"] = (
                chunk.metadata.industry
            )

        if chunk.metadata.document_type is not None:
            metadata["document_type"] = (
                chunk.metadata.document_type
            )

        if chunk.metadata.published_date is not None:
            metadata["published_date"] = (
                chunk.metadata.published_date.isoformat()
            )

        metadatas.append(
            metadata
        )

    _collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

def search_chunks(
    query_embedding: List[float],
    top_k: int = 3,
    industry: str = None,
):
    if top_k <= 0:
        raise ValueError(
            "top_k must be greater than 0."
        )

    where_filter = None

    if industry is not None:
        where_filter = {
            "industry": industry
        }

    results = _collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k,
        where=where_filter,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    return results