# Workflow – Kasparro Agentic Content Generation System

This document describes the **end-to-end execution workflow** of the Kasparro system using **LangGraph**.  

---

## 1. Execution Entry Point

The workflow is initiated via:

```bash
python runner.py
```

The runner:
- Loads input JSON files
- Initializes the shared `AgentState`
- Invokes the LangGraph DAG
- Persists final outputs and execution logs

No business logic or orchestration lives in `runner.py`.

---

## 2. Graph Initialization

The LangGraph is constructed using a predefined DAG:

- Nodes represent atomic agent actions
- Edges represent deterministic or conditional transitions
- The graph owns execution order entirely

Once invoked, execution proceeds **node by node**, passing the shared state forward.

---

## 3. Step-by-Step Workflow

### Step 1: Parse & Normalize Products
- Raw product JSONs are validated
- Products are normalized into a consistent internal schema
- Normalized data is stored in shared state

---

### Step 2: Generate Questions
- Categorized user questions are generated
- Initial attempt count is incremented
- Output is stored in state

---

### Step 3: Validate Question Count (Retry Gate)
- The number of generated questions is checked
- If below the minimum threshold:
  - Retry is triggered (if attempts < max)
  - Otherwise, retry is aborted gracefully
- Routing is handled via LangGraph conditional edges

---

### Step 4: Build FAQ Context
- Structured factual context is extracted
- No LLM calls occur at this stage
- Context is cached in state for reuse

---

### Step 5: Generate FAQ Answers
- Each question is answered independently
- LLM usage is strictly grounded in provided context
- Answers are accumulated in state

---

### Step 6: Assemble FAQ Page
- Questions and answers are assembled into final JSON
- Output structure is deterministic

---

### Step 7: Assemble Product Page
- Product details are assembled into structured JSON
- No LLM usage

---

### Step 8: Generate Comparison Page
- Two products are compared
- Deterministic fields (e.g., price) are handled directly
- Qualitative comparison uses an LLM
- Final output is templated into JSON

---

### Step 9: Schema Validation
- All output pages are validated using Pydantic schemas
- Errors are captured in state
- Execution completes gracefully regardless of validation result

---

## 4. Execution Logging

Every major step appends a message to the execution log.

The final log is persisted to:
```
data/output/execution_log.txt
```

This log provides a complete trace of the DAG execution.

---

## 5. Workflow Guarantees

- No custom control flow
- No agent-to-agent orchestration
- Explicit retry guards
- Deterministic execution order
- Transparent failure handling

---

## 6. Summary

This workflow ensures that content generation is:
- Agentic
- Robust
- Observable
- Framework-managed

The design aligns strictly with LangGraph best practices.
