# System Diagrams – Kasparro Agentic Content Generation System

This document describes the **LangGraph-based orchestration** used in the Kasparro Agentic Content Generation System.  

---

## 1. High-Level LangGraph DAG 

The system is orchestrated as a **directed acyclic graph (DAG)** managed entirely by LangGraph.  
There is **no custom sequential orchestration** and no agent-to-agent control flow.

```mermaid
flowchart TD
    A[Raw Product Inputs<br/>Primary + Comparison]
    B[Parse & Normalize<br/>ParserAgent]
    C[Generate Questions<br/>QuestionGenerationAgent]
    D[Validate Question Count<br/>Retry Guard]
    E[Generate Questions<br/>Retry Attempt]
    F[Build FAQ Context<br/>ContentLogicAgent]
    G[Generate FAQ Answers<br/>AnswerGenerationAgent]
    H[Assemble FAQ Page<br/>TemplateAgent]
    I[Assemble Product Page<br/>TemplateAgent]
    J[Generate Comparison Page<br/>ComparisonAgent + TemplateAgent]
    K[Schema Validation<br/>Pydantic]
    L[Final Outputs<br/>+ Execution Log]

    A --> B
    B --> C
    C --> D
    D -->|retry| E
    E --> D
    D -->|continue| F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
```

---

## 2. Conditional Routing & Retry Logic 

Question generation is protected by a **retry guard** implemented via LangGraph conditional edges.

```mermaid
flowchart TD
    Q[Generate Questions]
    V[Validate Question Count]

    Q --> V
    V -- count ≥ min_required_questions --> C[Continue DAG]
    V -- count < min_required_questions --> R{Attempts < max?}
    R -- Yes --> Q
    R -- No --> C
```

Key properties:
- Retry attempts are stored in shared state
- Maximum retries are enforced
- No infinite loops are possible
- Routing decisions are separated from state mutation

---

## 3. Shared State Flow

A single `AgentState` object flows through all nodes.

```mermaid
flowchart LR
    State[AgentState]

    State --> rawA[raw_product_a]
    State --> rawB[raw_product_b]
    State --> normA[normalized_product_a]
    State --> normB[normalized_product_b]
    State --> questions[generated_questions]
    State --> attempts[question_generation_attempts]
    State --> flags[retry_flags]
    State --> faqCtx[faq_context]
    State --> faqAns[faq_answers]
    State --> faqPage[faq_page]
    State --> prodPage[product_page]
    State --> compPage[comparison_page]
    State --> errors[schema_validation_errors]
    State --> log[execution_log]
```

This ensures transparency, debuggability, replayability, and framework-level observability.

---

## 4. Schema Validation Gate 

Before termination, all outputs pass through a **schema validation node**.

```mermaid
flowchart TD
    FAQ[FAQ Page]
    PROD[Product Page]
    COMP[Comparison Page]

    FAQ --> V[Schema Validation]
    PROD --> V
    COMP --> V

    V --> END[End of Graph]
```

- Validation is performed using **Pydantic schemas**
- Errors are captured in state
- The graph completes gracefully even on validation failure

---

## 5. Execution Logging

Each node appends a human-readable entry to the execution log.

```mermaid
sequenceDiagram
    participant Runner
    participant Graph
    participant State

    Runner->>Graph: invoke(state)
    Graph->>State: Parse Products
    Graph->>State: Generate Questions
    Graph->>State: Validate Question Count
    Graph->>State: Build FAQ Context
    Graph->>State: Generate FAQ Answers
    Graph->>State: Assemble Pages
    Graph->>State: Schema Validation
    Graph-->>Runner: Final State
```

The execution log is persisted to:
```
data/output/execution_log.txt
```

---