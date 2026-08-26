from app.services.chunking_service import chunk_document
from app.services.document_service import load_text_document
from app.services.embedding_service import embed_chunks
from app.services.vector_store_service import add_chunks


document = load_text_document(
    file_path="data/manufacturing_ai.txt",
    industry="manufacturing",
    document_type="research_report",
)

chunks = chunk_document(
    document=document,
    chunk_size=300,
    chunk_overlap=50,
)

embeddings = embed_chunks(
    chunks
)

add_chunks(
    chunks=chunks,
    embeddings=embeddings,
)

print(
    "Stored chunks:",
    len(chunks)
)