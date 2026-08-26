import numpy as np

from app.services.embedding_service import embed_text


text_a = (
    "Predictive maintenance helps identify "
    "equipment failures before breakdown."
)

text_b = (
    "Machine failure prediction can detect "
    "problems before equipment stops working."
)

text_c = (
    "Restaurants use fresh vegetables to "
    "prepare meals for customers."
)


embedding_a = np.array(
    embed_text(text_a)
)

embedding_b = np.array(
    embed_text(text_b)
)

embedding_c = np.array(
    embed_text(text_c)
)


def cosine_similarity(
    vector_a,
    vector_b
):
    return np.dot(
        vector_a,
        vector_b
    ) / (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )


similarity_ab = cosine_similarity(
    embedding_a,
    embedding_b
)

similarity_ac = cosine_similarity(
    embedding_a,
    embedding_c
)


print(
    "Maintenance vs machine failure:",
    similarity_ab
)

print(
    "Maintenance vs restaurant:",
    similarity_ac
)