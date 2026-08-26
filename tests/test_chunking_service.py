from app.models.document import (
    DocumentMetadata,
    IngestedDocument,
)
from app.services.chunking_service import (
    chunk_document,
)


def test_chunk_document_creates_multiple_chunks():

    document = IngestedDocument(
        content="A" * 1200,
        metadata=DocumentMetadata(
            source_id="source-1",
            source_name="test.txt",
            industry="manufacturing",
        ),
    )

    chunks = chunk_document(
        document,
        chunk_size=500,
        chunk_overlap=100,
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert chunk.content
        assert chunk.chunk_id
        assert (
            chunk.metadata.source_id
            == "source-1"
        )


def test_chunk_document_preserves_metadata():

    document = IngestedDocument(
        content=(
            "Predictive maintenance helps "
            "detect equipment failures."
        ),
        metadata=DocumentMetadata(
            source_id="source-123",
            source_name="manufacturing.txt",
            industry="manufacturing",
        ),
    )

    chunks = chunk_document(
        document,
        chunk_size=500,
        chunk_overlap=100,
    )

    assert len(chunks) == 1

    assert (
        chunks[0].metadata.source_name
        == "manufacturing.txt"
    )

    assert (
        chunks[0].metadata.industry
        == "manufacturing"
    )