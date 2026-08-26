import os
from typing import List

os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

from sentence_transformers import SentenceTransformer

from app.models.document import DocumentChunk
from app.config.settings import settings


MODEL_NAME = settings.EMBEDDING_MODEL

_model = SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> List[float]:
    if not text.strip():
        raise ValueError(
            "Cannot generate embedding for empty text."
        )

    embedding = _model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()


def embed_chunks(
    chunks: List[DocumentChunk],
) -> List[List[float]]:

    texts = [
        chunk.content
        for chunk in chunks
    ]

    if not texts:
        return []

    embeddings = _model.encode(
        texts,
        convert_to_numpy=True
    )

    return [
        embedding.tolist()
        for embedding in embeddings
    ]