from app.services.llm_service import (
    generate_research_result,
)
from app.services.retrieval_service import (
    retrieve_evidence,
)


query = (
    "What AI opportunities can help "
    "a manufacturing company?"
)


evidence = retrieve_evidence(
    query=query,
    top_k=3,
    industry="manufacturing",
)


print("Retrieved evidence:", len(evidence))


result = generate_research_result(
    query=query,
    evidence_items=evidence,
)


print("\nSUMMARY")
print(result.summary)


print("\nFINDINGS")

for finding in result.findings:
    print(
        "-",
        finding.title,
        finding.source_ids,
    )


print("\nOPPORTUNITIES")

for opportunity in result.opportunities:
    print(
        "-",
        opportunity.title,
        opportunity.expected_value,
        opportunity.source_ids,
    )


print("\nRISKS")

for risk in result.risks:
    print(
        "-",
        risk.title,
        risk.source_ids,
    )


print("\nCONFIDENCE")

print(result.confidence.level)
print(result.confidence.explanation)