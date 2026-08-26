from app.services.retrieval_service import retrieve_evidence


query = (
    "How can AI detect equipment "
    "failures before breakdown?"
)


evidence = retrieve_evidence(
    query=query,
    top_k=3,
    industry="manufacturing",
)


print("Query:", query)
print("Evidence count:", len(evidence))


for item in evidence:
    print("\n--------------------")
    print("Citation:", item.citation_id)
    print("Chunk ID:", item.chunk_id)
    print("Source:", item.source_name)
    print("Distance:", item.distance)
    print("Content:")
    print(item.content)