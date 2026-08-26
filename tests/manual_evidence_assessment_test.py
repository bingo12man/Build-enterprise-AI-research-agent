from app.services.evidence_service import (
    assess_evidence,
)
from app.services.retrieval_service import (
    retrieve_evidence,
)


query = (
    "What treatments are available "
    "for heart disease?"
)


evidence = retrieve_evidence(
    query=query,
    top_k=3,
    industry="manufacturing",
)


assessment = assess_evidence(
    evidence
)


print("Evidence count:")
print(
    assessment.evidence_count
)


print("\nDistances:")

for item in evidence:
    print(
        item.citation_id,
        item.distance,
    )


print("\nAverage distance:")
print(
    assessment.average_distance
)


print("\nEvidence level:")
print(
    assessment.level
)


print("\nExplanation:")
print(
    assessment.explanation
)

print("\nUnique sources:")
print(
    assessment.unique_source_count
)