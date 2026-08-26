from app.services.chunking_service import chunk_document
from app.services.document_service import load_text_document
from app.services.embedding_service import embed_chunks


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

embeddings = embed_chunks(chunks)


print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))

if embeddings:
    print(
        "Embedding dimension:",
        len(embeddings[0])
    )

    print(
        "First 10 values:",
        embeddings[0][:10]
    )