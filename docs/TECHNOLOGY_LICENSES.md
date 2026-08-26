# Enterprise AI Research Agent — Technology and Licence Inventory

## 1. Purpose

This document lists the main frameworks, libraries, models, databases, and external services used by the Enterprise AI Research Agent.

The project uses free, open-source, open-weight, or free-tier technologies suitable for the challenge MVP.

---

## 2. Core Technology Inventory

| Component | Technology | Purpose | Licence / Usage |
|---|---|---|---|
| Programming Language | Python | Core application development | Python Software Foundation License |
| API Framework | FastAPI | REST API layer | MIT |
| Frontend | Streamlit | Interactive research UI | Apache 2.0 |
| Validation | Pydantic | Request, response, and LLM schema validation | MIT |
| Embeddings Framework | SentenceTransformers | Text embeddings | Apache 2.0 |
| Embedding Model | `all-MiniLM-L6-v2` | Semantic similarity / retrieval | Verify exact model repository licence before submission |
| Vector Database | ChromaDB | Internal knowledge retrieval | Apache 2.0 |
| LLM SDK | Groq Python SDK | Access to Groq inference API | Apache 2.0 |
| LLM | `openai/gpt-oss-20b` | Research synthesis, evidence comparison, contradiction analysis | Apache 2.0 |
| Web Research | Tavily | External source search | External API / free-tier service terms |
| Relational Database | SQLite | Research history and source persistence | Public Domain |
| ASGI Server | Uvicorn | Local FastAPI server | BSD-style licence |
| Environment Config | python-dotenv | Local environment-variable loading | BSD-style licence |
| Testing | Pytest | Unit testing | MIT |
| ML Runtime | PyTorch | SentenceTransformer inference dependency | BSD-style licence |

---

## 3. FastAPI

FastAPI is used to provide the REST API layer.

Purpose:

```text
HTTP request
↓
Pydantic validation
↓
Research service
↓
Structured API response
```

Licence:

```text
MIT
```

---

## 4. Streamlit

Streamlit provides the interactive frontend and hosted challenge demo.

Purpose:

```text
Research question input
Research result display
Source display
Research history
```

Licence:

```text
Apache License 2.0
```

Streamlit Community Cloud is a hosted service and is governed separately by its service terms.

---

## 5. Pydantic

Pydantic provides deterministic schema validation.

Used for:

```text
ResearchRequest
ResearchResponse
EvidenceItem
EvidenceComparison
Contradiction
LLMResearchResult
```

Licence:

```text
MIT
```

---

## 6. SentenceTransformers

SentenceTransformers generates semantic embeddings for internal knowledge retrieval.

Current embedding model:

```text
all-MiniLM-L6-v2
```

Purpose:

```text
Research question
↓
Embedding vector
↓
ChromaDB similarity search
```

Framework licence:

```text
Apache License 2.0
```

The exact model licence should be checked against the specific `all-MiniLM-L6-v2` model repository used by the deployed application.

---

## 7. ChromaDB

ChromaDB stores internal document chunks and embeddings.

Purpose:

```text
Document chunks
+
Embedding vectors
+
Metadata
```

Licence:

```text
Apache License 2.0
```

---

## 8. Groq Python SDK

The application uses the Groq Python SDK to send inference requests.

Purpose:

```text
Evidence
↓
Groq API
↓
Structured LLM result
```

SDK licence:

```text
Apache License 2.0
```

Use of the hosted Groq API is also subject to Groq service terms.

---

## 9. gpt-oss-20b

Current model:

```text
openai/gpt-oss-20b
```

Used for:

```text
Evidence comparison
Contradiction detection
Research synthesis
Structured output
```

Model licence:

```text
Apache License 2.0
```

The model is accessed through Groq rather than hosted directly by this application.

---

## 10. Tavily

Tavily provides dynamic external research.

Purpose:

```text
Research question
↓
Web search
↓
Source title
URL
Evidence snippet
```

Tavily is used as an external API service.

The application uses the available free-tier service during the challenge MVP.

Tavily API usage is governed by Tavily's service terms rather than an open-source software licence for the hosted search service.

---

## 11. SQLite

SQLite stores:

```text
research_history
research_sources
```

SQLite is released into the public domain.

It is used because it provides lightweight persistent storage without requiring external infrastructure.

---

## 12. Pytest

Pytest provides automated unit testing.

Used for:

```text
chunking
evidence assessment
repository behavior
citation validation
```

Licence:

```text
MIT
```

---

## 13. Licence Summary

```text
FastAPI                 → MIT
Streamlit               → Apache 2.0
Pydantic                → MIT
SentenceTransformers    → Apache 2.0
ChromaDB                → Apache 2.0
Groq Python SDK         → Apache 2.0
gpt-oss-20b             → Apache 2.0
SQLite                  → Public Domain
Pytest                  → MIT
```

External hosted services such as Tavily and the Groq API are additionally governed by their respective service terms.

---

## 14. Challenge Compliance

The project does not require paid proprietary infrastructure to run the MVP.

The application primarily uses:

```text
Open-source software
Open-weight model
Free-tier APIs
Local persistence
Free Streamlit hosting
```

No API keys are stored in source control.

Secrets are provided using:

```text
.env
```

for local development and:

```text
Streamlit Secrets
```

for hosted deployment.

---

## 15. Verification Before Final Submission

Record exact installed package versions with:

```bash
pip freeze > installed-packages.txt
```

Inspect package metadata with:

```bash
pip show fastapi
pip show streamlit
pip show pydantic
pip show sentence-transformers
pip show chromadb
pip show groq
pip show tavily-python
pip show pytest
```

This allows the submitted licence inventory to be tied to the exact package versions used in the final application.
