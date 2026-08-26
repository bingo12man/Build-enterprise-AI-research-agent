from app.services.document_service import load_text_document


document = load_text_document(
    file_path="data/manufacturing_ai.txt",
    industry="manufacturing",
    document_type="research_report",
)

print(document)