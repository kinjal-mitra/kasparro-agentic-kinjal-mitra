# System Diagrams – Kasparro Agentic Content Generation System

This document describes the **LangGraph-based orchestration** used in the Kasparro Agentic Content Generation System.  
All diagrams reflect the **current architecture**, which uses a **stateful DAG**, conditional routing, retry guards, and schema validation.

---

## 1. High-Level LangGraph DAG

The system is orchestrated as a **directed acyclic graph (DAG)** managed entirely by LangGraph.  
There is **no custom sequential orchestration** and no agent-to-agent control flow.

```
┌──────────────────────────┐
│   Raw Product Inputs     │
│ (Primary + Comparison)   │
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Parse & Normalize Node   │
│ (ParserAgent)            │
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Generate Questions Node  │
│ (QuestionGenerationAgent)│
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Validate Question Count  │
│ (Retry Guard)            │
└──────────────────────────┘__
        │retry                │continue
        ↓                     ↓
┌──────────────────┐   ┌──────────────────────────┐
│Generate Questions│   │ Build FAQ Context Node   │
│(Retry Attempt)   │   │ (ContentLogicAgent)      │
└──────────────────┘   └─────────────┬────────────┘
                                     ↓
                          ┌──────────────────────────┐
                          │ Generate FAQ Answers     │
                          │ (AnswerGenerationAgent)  │
                          └─────────────┬────────────┘
                                        ↓
                          ┌──────────────────────────┐
                          │ Assemble FAQ Page        │
                          │ (TemplateAgent)          │
                          └─────────────┬────────────┘
                                        ↓
                          ┌──────────────────────────┐
                          │ Assemble Product Page    │
                          │ (TemplateAgent)          │
                          └─────────────┬────────────┘
                                        ↓
                          ┌──────────────────────────┐
                          │ Generate Comparison Page │
                          │ (ComparisonAgent +       │
                          │  TemplateAgent)          │
                          └─────────────┬────────────┘
                                        ↓
                          ┌──────────────────────────┐
                          │ Schema Validation Node   │
                          │ (Pydantic Validation)   │
                          └─────────────┬────────────┘
                                        ↓
                          ┌──────────────────────────┐
                          │ Final Outputs            │
                          │ + Execution Log          │
                          └──────────────────────────┘
```

---

## 2. Conditional Routing & Retry Logic

Question generation is protected by a **retry guard** implemented via LangGraph conditional edges.

### Retry Logic Flow

```
Generate Questions
        ↓
Validate Question Count
        ↓
Is count ≥ min_required_questions?
        ├── Yes → Continue DAG
        └── No  → Retry (if attempts < max)
                    └── Else → Abort retry and continue
```

Key properties:
- Retry attempts are stored in shared state
- Maximum retries are enforced
- No infinite loops are possible
- Routing decisions are separated from state mutation

---

## 3. Shared State Flow

A single `AgentState` object flows through all nodes.

```
AgentState
├── raw_product_a
├── raw_product_b
├── normalized_product_a
├── normalized_product_b
├── generated_questions
├── question_generation_attempts
├── retry_flags
├── faq_context
├── faq_answers
├── faq_page
├── product_page
├── comparison_page
├── schema_validation_errors
└── execution_log
```

This ensures:
- Transparency
- Debuggability
- Replayability
- Framework-level observability

---

## 4. Schema Validation Gate

Before termination, all outputs pass through a **schema validation node**.

```
FAQ Page ─────────┐
Product Page ─────┼──▶ Schema Validation ─▶ End
Comparison Page ──┘
```

- Validation is performed using **Pydantic schemas**
- Errors are captured in state
- The graph completes gracefully even on validation failure

---

## 5. Execution Logging

Each node appends a human-readable entry to the execution log.

```
Example Execution Log
[Parse Products]
[Generate Questions – Attempt 1]
[FAQ Count Validated]
[Build FAQ Context]
[Generate FAQ Answers]
[Assemble FAQ Page]
[Assemble Product Page]
[Generate Comparison Page]
[Schema Validation Successful]
```

The log is persisted as:
```
data/output/execution_log.txt
```

---

