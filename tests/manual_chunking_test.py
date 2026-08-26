from app.services.chunking_service import chunk_document
from app.services.document_service import load_text_document


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

print("Number of chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print("\n--------------------")
    print("Chunk:", index)
    print("Chunk ID:", chunk.chunk_id)
    print("Source:", chunk.metadata.source_name)
    print("Industry:", chunk.metadata.industry)
    print("Content:")
    print(chunk.content)