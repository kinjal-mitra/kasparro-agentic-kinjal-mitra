# Orchestration Notes – Kasparro Agentic Content Generation System

This document explains **how orchestration is handled** in the Kasparro system and explicitly documents design decisions made to comply with agentic system requirements.

---

## 1. Orchestration Philosophy

The system deliberately avoids:
- Manual sequencing
- Custom pipelines
- Agent-to-agent invocation

Instead, **LangGraph** is used as the single orchestration authority.

Agents are treated as:
- Stateless workers
- Pure functions over shared state

---

## 2. Why LangGraph

LangGraph was chosen to satisfy the following requirements:

- Explicit shared state
- Deterministic execution graph
- Conditional routing
- Retry guards
- Framework-level validation

This ensures the system is:
- Auditable
- Replayable
- Extensible

---

## 3. Separation of Concerns

| Layer | Responsibility |
|------|---------------|
| Runner | I/O, initialization, persistence |
| LangGraph | Control flow, routing, retries |
| Agents | Atomic reasoning or transformation |
| Templates | Output structure |
| Schemas | Validation and correctness |

No layer violates its responsibility.

---

## 4. State-Driven Control Flow

All control decisions are based on **state**, not return values.

Examples:
- Retry decisions depend on counters in state
- Routing functions read state but do not mutate it
- Nodes mutate state but do not control routing

This separation is required by LangGraph design.

---

## 5. Conditional Routing

Retry logic is implemented via:

- A validation node that updates retry flags
- A router function that returns routing keys
- Conditional edges defined at graph construction time

This ensures:
- No hidden branching
- No infinite loops
- Fully visible execution paths

---

## 6. Failure Handling Strategy

Failures are handled gracefully:

- Errors are recorded in state
- Execution continues to termination
- Outputs and logs remain available for inspection

The system does not crash on partial failure.

---

## 7. Observability

Observability is achieved through:

- Execution logs stored in state
- Persisted logs written to disk
- Deterministic node boundaries

This makes debugging and evaluation straightforward.

---

