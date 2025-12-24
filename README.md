# Kasparro – Agentic Content Generation System

A modular **multi-agent content generation pipeline** that transforms structured product data into **machine-readable content pages** (FAQ, Product Page, Comparison Page) using clean agent boundaries and deterministic logic.

This project is built as part of the **Kasparro – Applied AI Engineer Challenge**.

---

## 🎯 Objective

Design and implement a **production-style agentic system** that:
- Parses product data
- Generates categorized user questions
- Applies reusable content logic blocks
- Assembles structured JSON pages
- Runs end-to-end via agent orchestration (not a monolith)

---

## 🧠 System Overview

The system follows a **clear agent pipeline**:

ParserAgent <br>
↓<br>
QuestionGenerationAgent <br>
↓<br>
ContentLogicAgent <br>
↓<br>
TemplateAgent <br>
↓<br>
ComparisonAgent <br>
↓<br>
SerializationAgent <br>


Each agent has a **single responsibility**, strict input/output contracts, and no hidden global state.

---

## 🧩 Key Agents

- **ParserAgent**  
  Normalizes raw product input into a canonical schema.

- **QuestionGenerationAgent**  
  Generates categorized, human-readable user questions using a deterministic baseline with optional LLM expansion.

- **ContentLogicAgent**  
  Produces answers using reusable, rule-based content logic blocks.

- **TemplateAgent**  
  Assembles final page-level JSON structures (FAQ, Product, Comparison).

- **ComparisonAgent**  
  Compares the main product with a fictional alternative using the same normalized schema.

- **SerializationAgent**  
  Writes clean, validated JSON outputs to disk.

---

## 📁 Output

The pipeline generates the following machine-readable files:

data/output/

├── faq.json <br>
├── product_page.json <br>
└── comparison_page.json


---

## ▶️ How to Run

```bash
python runner.py
```

The pipeline is OS-agnostic and uses pathlib for file handling.

---

## ✅ Design Principles

- Strong separation of concerns

- Deterministic core with optional LLM usage

- Reusable logic blocks

- Schema-safe agent communication

- Fully testable and extensible architecture
---

## 📌 Notes

- No external data or research is used

- Product B in comparisons is fictional but structured

- All outputs are strict JSON (no free text)
---

## 📄 Documentation

- Detailed system design and assumptions are available in:

```bash
docs/projectdocumentation.md
```