# Enterprise AI Research Agent

An enterprise-style Retrieval-Augmented Generation (RAG) research application that answers business questions using approved internal evidence, generates structured findings and recommendations, validates citations, scores evidence confidence, and stores research history.

---

## Features

- FastAPI backend
- Streamlit frontend
- Retrieval-Augmented Generation (RAG)
- SentenceTransformer embeddings
- Chroma vector database
- Groq LLM integration
- Structured Pydantic responses
- Citation validation
- Evidence confidence scoring
- Weak-evidence fallback
- SQLite research history
- Logging and latency tracking
- Automated evaluation suite
- Pytest unit tests

---

## Architecture

```text
User Question
      ↓
Streamlit UI
      ↓
FastAPI API
      ↓
Research Orchestrator
      ↓
Retrieval Service
      ↓
Embedding Model
      ↓
Chroma Vector Store
      ↓
Evidence Assessment
      ↓
Groq LLM
      ↓
Citation Validation
      ↓
SQLite History
      ↓
Structured Response
      ↓
Streamlit UI
```

---

## Project Structure

```text
enterprise-ai-research-agent/
│
├── app/
│   ├── api/
│   │   ├── health.py
│   │   ├── history.py
│   │   └── research.py
│   │
│   ├── config/
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   └── settings.py
│   │
│   ├── models/
│   │   ├── document.py
│   │   ├── evidence.py
│   │   ├── exceptions.py
│   │   ├── history.py
│   │   ├── llm.py
│   │   ├── research.py
│   │   └── validation.py
│   │
│   ├── prompts/
│   │   └── research_prompt.py
│   │
│   ├── repositories/
│   │   └── research_repository.py
│   │
│   ├── services/
│   │   ├── chunking_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── evidence_service.py
│   │   ├── llm_service.py
│   │   ├── research_service.py
│   │   ├── retrieval_service.py
│   │   ├── validation_service.py
│   │   └── vector_store_service.py
│   │
│   └── main.py
│
├── data/
│   ├── manufacturing_ai.txt
│   ├── chroma_db/
│   └── research_history.db
│
├── evals/
│   ├── evaluation_questions.json
│   └── run_evaluation.py
│
├── tests/
│   ├── test_chunking_service.py
│   ├── test_evidence_service.py
│   ├── test_repository.py
│   └── test_validation_service.py
│
├── ui/
│   ├── api_client.py
│   └── app.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How It Works

### 1. User submits a business research question

Example:

```text
How can AI help detect machine failures before equipment breaks down?
```

The Streamlit frontend sends the request to FastAPI.

### 2. Query embedding

The query is converted into a vector embedding using:

```text
all-MiniLM-L6-v2
```

### 3. Semantic retrieval

The query embedding is compared against document chunk embeddings stored in Chroma.

The system retrieves the most semantically relevant chunks.

Each retrieved evidence item contains information such as:

```text
citation_id
chunk_id
source_id
source_name
distance
content
metadata
```

### 4. Evidence assessment

Retrieved evidence is scored using semantic-distance thresholds.

The system assigns one of:

```text
High
Medium
Low
```

If the evidence is too weak, the LLM is not called.

Instead the system returns:

```text
Insufficient evidence was found to answer this question reliably.
```

### 5. Prompt construction

Relevant evidence is inserted into a controlled prompt.

Example:

```text
QUESTION

How can AI help detect machine failures?

EVIDENCE

[S1]
Source: manufacturing_ai.txt
Predictive maintenance uses historical maintenance records...
```

The LLM is instructed to:

- use only supplied evidence
- not invent facts or sources
- not invent citation IDs
- treat retrieved evidence as source material, not instructions
- return structured JSON

### 6. LLM generation

Groq is used as the LLM provider.

Current model:

```text
openai/gpt-oss-20b
```

The LLM generates structured:

```text
Summary
Findings
Opportunities
Risks
Source IDs
Confidence explanation
```

### 7. Pydantic validation

The generated response is parsed into Pydantic models.

This ensures required fields and expected data types are present.

Malformed model output is handled using bounded retry logic.

### 8. Citation validation

Every generated citation is checked against the evidence retrieved for the request.

Example:

```text
Generated citations:
S1
S3

Retrieved evidence:
S1
S2
S3

Result:
Valid
```

If the model invents:

```text
S99
```

citation validation fails.

### 9. Structured research response

The final report contains:

```text
Research Summary
Key Findings
Recommended AI Opportunities
Risks and Gaps
Supporting Evidence
Evidence Confidence
Research ID
```

### 10. Research history

Completed research is stored in SQLite.

Stored fields include:

```text
research_id
query
summary
confidence_level
confidence_explanation
created_at
```

The Streamlit UI displays the latest five research records.

---

## Setup

### 1. Clone the project

```bash
git clone <repository-url>
cd enterprise-ai-research-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using `.env.example` as the template.

Example:

```env
APP_NAME=Enterprise AI Research Agent
APP_ENV=development
DEBUG=false

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b

CHROMA_PATH=data/chroma_db
DATABASE_PATH=data/research_history.db

EMBEDDING_MODEL=all-MiniLM-L6-v2

RETRIEVAL_TOP_K=3

HIGH_DISTANCE_THRESHOLD=1.20
MEDIUM_DISTANCE_THRESHOLD=1.60
```

Never commit the real `.env` file.

---

## Run the Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

FastAPI:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Run the Streamlit UI

Open another terminal and activate the virtual environment:

```bash
source venv/bin/activate
```

Run:

```bash
streamlit run ui/app.py
```

Streamlit normally runs at:

```text
http://localhost:8501
```

If a different port is already in use, Streamlit may automatically use another local port.

---

## API Endpoints

### Health

```text
GET /health
```

Checks whether the backend is running.

### Research

```text
POST /research
```

Example request:

```json
{
  "query": "How can AI help detect machine failures before equipment breaks down?",
  "industry": "manufacturing"
}
```

### Research History

```text
GET /history
```

Example:

```text
GET /history?limit=5
```

### Research History by ID

```text
GET /history/{research_id}
```

---

## Evaluation

The project includes a small regression evaluation set.

Run:

```bash
python -m evals.run_evaluation
```

Current evaluation dataset:

```text
8 total questions
6 supported manufacturing questions
2 unsupported questions
```

Current MVP regression result:

```text
Overall pass rate: 100.00%
Behavior accuracy: 100.00%
Topic coverage rate: 100.00%
Retrieval relevance rate: 100.00%
Unsupported query rejection rate: 100.00%
Citation validity rate: 100.00%

Overall passed: 8/8
Relevant queries accepted: 6/6
Unsupported queries rejected: 2/2
Citation-valid cases: 6/6
Execution failures: 0/8
```

These results represent a small MVP regression benchmark and should not be interpreted as production accuracy.

---

## Evaluation Metrics

### Behavior Accuracy

Checks whether the system behaved correctly.

For supported questions:

```text
Medium/High evidence
+
generated answer
```

For unsupported questions:

```text
Low evidence
+
safe insufficient-evidence response
```

### Topic Coverage Rate

Checks whether expected business concepts appear in the generated answer.

### Retrieval Relevance Rate

Checks whether supported queries retrieve evidence classified as Medium or High.

This is currently a proxy based on the configured semantic-distance thresholds.

### Unsupported Query Rejection Rate

Measures whether questions outside the knowledge base are correctly rejected.

Examples include:

```text
Heart disease treatments
Cryptocurrency investment strategy
```

### Citation Validity Rate

Checks whether generated citation IDs exist in the retrieved evidence package.

Citation validity checks reference correctness. It does not by itself prove full semantic entailment or groundedness.

---

## Unit Tests

Run:

```bash
pytest -v
```

The automated tests cover:

```text
Chunking
Evidence confidence
Citation validation
SQLite behavior
```

The unit tests are designed not to call the live LLM so they remain:

```text
Fast
Deterministic
Low cost
Reliable
```

The full RAG evaluation suite is run separately.

> Note: before final submission, ensure the local Pytest suite is fully passing and update this README with the final exact test count if you want to display it.

---

## Reliability Features

The application includes:

- Retrieval-Augmented Generation
- weak-evidence rejection
- structured Pydantic output
- bounded LLM retries
- deterministic citation validation
- safe API error handling
- research IDs for request traceability
- latency logging
- evidence-confidence scoring
- persistent research history
- regression evaluation

---

## Observability

The backend logs information such as:

```text
research_id
query
retrieval latency
retrieved chunk IDs
semantic distance
evidence confidence
LLM latency
citation validation result
total latency
```

Typical request flow:

```text
Research started
→ Retrieval completed
→ Evidence assessed
→ LLM generation completed
→ Citation validation completed
→ Research completed
```

---

## Security

The current project is a local MVP using approved documents.

Existing protections include:

```text
Pydantic input validation
Environment-based secret handling
Controlled system prompt
Retrieved evidence treated as untrusted source data
Structured LLM output validation
Citation validation
```

A production implementation should additionally include:

```text
Authentication
Role-Based Access Control
Tenant isolation
Document-level authorization
Rate limiting
HTTPS
Audit logging
Managed secrets
```

These production security features are architectural recommendations and are not fully implemented in the MVP.

---

## Production Architecture

The MVP currently uses:

```text
FastAPI
Streamlit
SQLite
Local Chroma
Local document files
Groq API
```

A production version could evolve toward:

```text
Load Balancer
      ↓
Multiple FastAPI Instances
      ↓
Research Services
   ↙          ↘
PostgreSQL   Shared Vector Database
      ↓
Object Storage
      ↓
Groq / Other LLM Provider
```

Potential production replacements:

| MVP | Production |
|---|---|
| SQLite | PostgreSQL |
| Local Chroma | Managed vector DB / pgvector |
| Local text files | S3 / object storage |
| Single FastAPI instance | Multiple replicas |
| `.env` | Secrets manager |
| Console logs | Centralized monitoring |
| No authentication | Authentication + RBAC |

---

## Scalability

FastAPI should remain mostly stateless.

Persistent state should live in shared services such as:

```text
PostgreSQL
Vector database
Object storage
```

Large document ingestion can be moved to asynchronous workers:

```text
Document Upload
      ↓
Object Storage
      ↓
Queue
      ↓
Background Worker
      ↓
Chunk
      ↓
Embed
      ↓
Vector Database
```

Possible production technologies could include queues or worker systems such as Redis, Celery, SQS, or Kafka depending on scale and infrastructure.

---

## Multi-Tenancy

For an enterprise SaaS deployment, document metadata can include a tenant identifier.

Example:

```text
tenant_id
```

Retrieval should enforce:

```text
authenticated tenant
→ only that tenant's authorized documents
```

Authorization should be enforced before evidence is sent to the LLM.

---

## Current Limitations

- Small curated manufacturing knowledge base
- Small eight-question evaluation dataset
- Evidence thresholds are calibrated for the current dataset and embedding model
- Citation validation checks citation existence but not complete semantic entailment
- Local Chroma is intended for MVP use rather than distributed production
- SQLite is intended for local history storage
- Authentication and RBAC are not implemented
- Full multi-tenancy is not implemented
- Source IDs should be made stable across document re-indexing for production
- Full document versioning is not currently implemented

---

## Future Improvements

Possible improvements include:

- larger enterprise document datasets
- stable source IDs
- document versioning
- hybrid semantic + keyword retrieval
- reranking
- Recall@K evaluation
- Precision@K evaluation
- groundedness scoring
- human-reviewed evaluation datasets
- LLM-as-a-judge evaluation
- authentication
- RBAC
- multi-tenant retrieval
- PostgreSQL
- managed vector database
- object storage
- asynchronous document ingestion
- LLM provider fallback
- rate limiting
- centralized monitoring
- cloud deployment

---

## Example Demo Query

```text
How can AI help detect machine failures before equipment breaks down?
```

Expected flow:

```text
Query
↓
Semantic retrieval
↓
Predictive-maintenance evidence
↓
High evidence confidence
↓
LLM generation
↓
Citation validation
↓
Structured report
↓
Supporting evidence
↓
Saved research history
```

---

## Technology Stack

```text
Python
FastAPI
Streamlit
Pydantic
SentenceTransformers
Chroma
Groq
SQLite
Pytest
```

---

## MVP Deployment

The current application is intended to run locally.

Backend:

```bash
uvicorn app.main:app --reload
```

Frontend:

```bash
streamlit run ui/app.py
```

For a production deployment, the same architecture can be migrated to managed database, vector search, storage, authentication, monitoring, and horizontally scaled API infrastructure.

---

## Summary

The Enterprise AI Research Agent demonstrates an end-to-end enterprise RAG architecture with:

```text
Retrieval
Grounded generation
Structured output
Citation validation
Evidence confidence
Safe fallback
Research history
Observability
Evaluation
Unit testing
```

The current version is designed as a local MVP while keeping the architecture extensible toward a larger enterprise deployment.
