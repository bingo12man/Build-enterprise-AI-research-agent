from app.services.embedding_service import embed_text
from app.services.vector_store_service import search_chunks


query = (
    "How can AI help identify machine "
    "failures before equipment breaks down?"
)


query_embedding = embed_text(
    query
)


results = search_chunks(
    query_embedding=query_embedding,
    top_k=3,
    industry="manufacturing",
)


print(
    "Query:",
    query
)


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for index, (
    document,
    metadata,
    distance,
) in enumerate(
    zip(
        documents,
        metadatas,
        distances,
    ),
    start=1,
):
    print("\n--------------------")
    print("Result:", index)
    print("Distance:", distance)
    print(
        "Source:",
        metadata["source_name"]
    )
    print("Content:")
    print(document)