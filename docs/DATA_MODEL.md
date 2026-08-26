# Enterprise AI Research Agent — Data Model

## 1. Overview

The application stores two types of persistent structured data:

1. Research history
2. Evidence/source records

Internal document embeddings are stored separately in ChromaDB.

The data model is designed to maintain traceability between a research question, the generated answer, and the evidence used to support that answer.

---

## 2. Relational Data Model

```text
┌──────────────────────────┐
│     research_history     │
├──────────────────────────┤
│ research_id PK           │
│ query                    │
│ summary                  │
│ confidence_level         │
│ confidence_explanation   │
│ created_at               │
└────────────┬─────────────┘
             │
             │ research_id
             │
             ▼
┌──────────────────────────┐
│     research_sources     │
├──────────────────────────┤
│ id PK                    │
│ research_id FK           │
│ citation_id              │
│ source_id                │
│ source_name              │
│ source_type              │
│ source_url               │
│ evidence_text            │
│ created_at               │
└──────────────────────────┘