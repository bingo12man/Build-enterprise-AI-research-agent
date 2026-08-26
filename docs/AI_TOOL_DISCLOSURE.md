# Enterprise AI Research Agent — AI Tool Disclosure

## 1. Purpose

This document discloses how AI-assisted development tools were used while building the Enterprise AI Research Agent.

The final system design, implementation choices, debugging decisions, testing, and deployment steps were reviewed and understood by the developer.

---

## 2. AI Tools Used

AI assistance was used during development for:

- architecture planning
- code drafting
- refactoring suggestions
- debugging
- test planning
- documentation
- deployment troubleshooting
- interview / technical validation preparation

---

## 3. How AI Assistance Was Used

Examples include:

```text
Designing the service-layer architecture
Planning the RAG pipeline
Drafting Pydantic models
Reviewing retrieval logic
Designing citation validation
Adding evidence comparison
Adding contradiction detection
Debugging SQLite persistence
Improving README documentation
Preparing architecture explanations
```

AI suggestions were treated as implementation assistance rather than automatically accepted output.

---

## 4. Developer Responsibilities

The developer was responsible for:

```text
Selecting the architecture
Setting up the project
Configuring APIs
Running and testing code
Debugging runtime errors
Validating research outputs
Reviewing model behavior
Deploying the application
Verifying persistence
Explaining design trade-offs
```

The developer can explain the purpose and behavior of the major components used in the system.

---

## 5. Areas Implemented and Validated

The following capabilities were implemented and tested as part of the project:

```text
FastAPI backend
Streamlit frontend
Document ingestion
Chunking
SentenceTransformer embeddings
ChromaDB retrieval
Tavily external research
Evidence merging
Evidence assessment
Evidence comparison
Contradiction detection
Groq LLM synthesis
Citation validation
SQLite research history
SQLite source persistence
Logging
Evaluation
Cloud deployment
```

---

## 6. Human Review

AI-generated code suggestions were reviewed before being integrated.

Development included direct manual testing such as:

```text
Running Python modules
Executing research queries
Inspecting retrieved evidence
Checking citations
Testing web research
Testing contradiction analysis
Inspecting SQLite records
Restarting Python and verifying persistence
Testing the deployed Streamlit application
```

---

## 7. Known Limitations

The developer also identified limitations rather than relying on AI-generated claims.

Examples include:

```text
Small internal knowledge base
Duplicate internal retrieval results
Limited unit-test cleanup remaining
SQLite not suitable for large-scale production
No authentication / RBAC
No full multi-tenancy
No complete semantic entailment checking
Limited source-quality ranking
```
---

## 8. Disclosure Statement

AI coding tools were used as development assistants for planning, coding support, debugging, documentation, and preparation.

The submitted application was manually run, tested, reviewed, and deployed by the developer.

The developer remains responsible for understanding and explaining the architecture, implementation, behavior, limitations, and design trade-offs of the final system.
