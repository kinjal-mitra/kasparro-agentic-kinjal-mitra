# Kasparro – Agentic Content Generation System (LangGraph)

This repository implements a **stateful, agentic content generation system** built using **LangGraph** as part of the **Kasparro – Applied AI Engineer Challenge**.

The system ingests structured product data and autonomously generates multiple **machine-readable content pages** (FAQ, Product Page, Comparison Page) using:

- Graph-based agent orchestration (LangGraph)
- Explicit shared state
- Conditional execution & retry guards
- Schema-validated outputs
- Deterministic templates
- LLM-powered reasoning where appropriate

This implementation **strictly avoids custom sequential orchestration** and instead relies on a **framework-managed agentic DAG**.

---

## 🎯 Objective

Automatically generate structured content pages from a small product dataset using a **true agentic framework**, not a monolithic LLM script.

The system produces:
- **FAQ Page** – categorized questions with LLM-generated answers
- **Product Page** – structured product description
- **Comparison Page** – LLM-assisted comparison against a fictional product

All outputs are produced as **clean, schema-validated JSON files** suitable for downstream systems.

---

## 🚀 How to Run

```bash
git clone https://github.com/kinjal-mitra/kasparro-agentic-kinjal-mitra.git
cd kasparro-agentic-kinjal-mitra
pip install -r requirements.txt
python runner.py
```

---

## 🧪 Testing

Tests validate **LangGraph execution**, retry guards, and schema enforcement.

```bash
pytest tests/
```

---

## 🧠 Core Architecture 

This system is implemented as a **LangGraph DAG** with:

- Explicit **AgentState**
- Deterministic node boundaries
- Conditional routing
- Retry guards
- Final schema validation gate

### High-Level DAG Flow

```text
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

## 🧩 Agentic Design

### Shared State
All agents operate on a shared **AgentState**, which includes:
- Normalized product data
- Generated questions & answers
- Retry counters & guardrails
- Execution log
- Final output pages
- Schema validation errors (if any)

### Conditional Logic
- FAQ generation retries are **state-driven**
- Retry attempts are capped to prevent infinite loops
- Routing decisions are separated from state mutation (LangGraph best practice)

---

## 🤖 Key Agents & Responsibilities

- **ParserAgent** – Normalizes raw product input into a consistent internal schema.
- **QuestionGenerationAgent** – Generates categorized user questions.
- **ContentLogicAgent** – Extracts structured factual context.
- **AnswerGenerationAgent** – Generates answers using LLMs.
- **ComparisonAgent** – Compares two products.
- **TemplateAgent** – Assembles final JSON pages.
- **SerializationAgent** – Writes outputs to disk.

---

## 🛡️ Robustness & Guarantees

- Retry guard
- Schema validation (Pydantic)
- Execution logs
- Framework-level error handling

---

## 📦 Outputs

```text
data/output/
├── faq.json
├── product_page.json
├── comparison_page.json
└── execution_log.txt
```

---




