import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "Enterprise AI Research Agent",
    )

    APP_ENV = os.getenv(
        "APP_ENV",
        "development",
    )

    DEBUG = os.getenv(
        "DEBUG",
        "false",
    ).lower() == "true"

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
    )

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    )

    CHROMA_PATH = os.getenv(
        "CHROMA_PATH",
        "data/chroma_db",
    )

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        "data/research_history.db",
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2",
    )

    RETRIEVAL_TOP_K = int(
        os.getenv(
            "RETRIEVAL_TOP_K",
            "3",
        )
    )

    HIGH_DISTANCE_THRESHOLD = float(
        os.getenv(
            "HIGH_DISTANCE_THRESHOLD",
            "1.20",
        )
    )

    MEDIUM_DISTANCE_THRESHOLD = float(
        os.getenv(
            "MEDIUM_DISTANCE_THRESHOLD",
            "1.60",
        )
    )


settings = Settings()