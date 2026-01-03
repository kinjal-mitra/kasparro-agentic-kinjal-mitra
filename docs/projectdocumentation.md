# Project Documentation – Kasparro Agentic Content Generation System

## 1. Problem Statement

The goal of this project is to design and implement a **true agentic content generation system** that transforms structured product data into multiple machine-readable content pages (FAQ, Product Page, and Comparison Page).  
The system must avoid monolithic scripts and instead use a **framework-driven, stateful agent orchestration** approach.

---

## 2. Expected Inputs

### Primary Inputs
- `data/input/product_data.json`  
  Structured JSON describing a skincare product.

- `data/input/fictitious_product.json`  
  A second (fictional) product used for comparison.

### Environment Variables
- `ANTHROPIC_API_KEY` – for FAQ answer generation
- `GROQ_API_KEY` – for fast comparison reasoning

---

## 3. Expected Outputs

All outputs are written to `data/output/`:

- `faq.json` – FAQ page with categorized questions and answers
- `product_page.json` – Structured product description
- `comparison_page.json` – Product-to-product comparison
- `execution_log.txt` – Full execution trace of the agentic DAG

All output files are **schema-validated JSON**.

---

## 4. Architecture Overview (LangGraph-Based)

This system is implemented using **LangGraph**, ensuring:
- Explicit shared state
- Deterministic DAG execution
- Conditional routing
- Retry guards
- Framework-level validation

### High-Level DAG Flow

```
Raw Product Inputs
        ↓
Parse & Normalize Products
        ↓
Generate Questions
        ↓
Validate Question Count
   ┌───────────────┐
   │ Retry (≤ N)   │
   └──────┬────────┘
          ↓
Build FAQ Context
        ↓
Generate FAQ Answers
        ↓
Assemble FAQ Page
        ↓
Assemble Product Page
        ↓
Generate Comparison Page
        ↓
Schema Validation
        ↓
Final Outputs
```

---

## 5. Agent State Design

All agents operate on a shared `AgentState`, which includes:

- Raw and normalized product data
- Generated questions and answers
- Retry counters and guard thresholds
- Execution log
- Final output pages
- Schema validation errors (if any)

This ensures **transparent, debuggable, and replayable execution**.

---

## 6. Agent Responsibilities

### ParserAgent
- Validates raw input
- Produces normalized product schema

### QuestionGenerationAgent
- Generates categorized questions
- Supports retry if minimum count is not met

### ContentLogicAgent
- Extracts structured factual context
- No LLM usage

### AnswerGenerationAgent
- Uses LLM to generate grounded answers
- No orchestration logic

### ComparisonAgent
- Performs deterministic and LLM-assisted comparison

### TemplateAgent
- Assembles final JSON pages
- Enforces structural consistency

### SerializationAgent
- Writes outputs to disk
- Handles filesystem concerns only

---

## 7. Robustness & Safety Mechanisms

- **Retry Guard**: Prevents infinite loops during question generation
- **Schema Validation**: Final outputs validated using Pydantic
- **Execution Logs**: Full trace saved to file
- **Framework-Level Routing**: No custom control flow

---

## 8. Testing Strategy

Tests are written against **LangGraph execution**, not individual agents.

Validated aspects:
- End-to-end DAG execution
- Retry guard enforcement
- Output schema correctness

This ensures tests reflect **system behavior**, not implementation details.

---