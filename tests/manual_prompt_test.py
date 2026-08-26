from app.prompts.research_prompt import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from app.services.retrieval_service import (
    retrieve_evidence,
)


query = (
    "What AI opportunities can help "
    "reduce manufacturing downtime?"
)


evidence = retrieve_evidence(
    query=query,
    top_k=3,
    industry="manufacturing",
)


user_prompt = build_user_prompt(
    query=query,
    evidence_items=evidence,
)


print("SYSTEM PROMPT")
print("-------------")
print(SYSTEM_PROMPT)

print("\nUSER PROMPT")
print("-----------")
print(user_prompt)