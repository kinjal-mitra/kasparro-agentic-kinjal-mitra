# Kasparro – Agentic Content Generation System

This repository implements a **multi-agent, modular content generation pipeline** built as part of the **Kasparro – Applied AI Engineer Challenge**.

The system ingests a small, structured product dataset and autonomously generates multiple **machine-readable content pages** (FAQ, Product Page, Comparison Page) using agent orchestration, reusable logic blocks, and template-driven assembly.

---

## 🎯 Objective

Automatically generate structured content pages from a small product dataset using a **multi-agent pipeline**, without relying on a monolithic LLM script.

The system produces:
- FAQ Page (question-aware, LLM-generated answers)
- Product Description Page
- Comparison Page (against a fictional product)

All outputs are generated as **clean JSON files**.

---
## 🚀 How to Run

1. Place product data in:
   ```
    data/input/product_data.json

2. Run:
   ```
    python runner.py
  
3. Outputs will be written to:
   ```
    data/output/
   

---
```bash

## 🧩 High-Level Architecture


Raw Product Data
      ↓
 Parser Agent
      ↓
Normalized Internal Product Model
      ↓
+----------------------------+
| Question Generation Agent  |
| Content Logic Agent        |
| Comparison Agent           |
| Answer Generation Agent    |
+----------------------------+
      ↓
 Template Agent
      ↓
 Serialization Agent
      ↓
 JSON Outputs
```
---

## 🤖 Key Agents

- **ParserAgent**  
  Normalizes raw product input into an internal schema.

- **QuestionGenerationAgent**  
  Generates categorized, human-readable user questions (rule-based + optional LLM expansion).

- **ContentLogicAgent**  
  Extracts structured, category-specific factual context from product data.

- **Comparison Agent**
  Compares the given product and a fictitious product using a LLM.

- **AnswerGenerationAgent**  
  Uses the LLM to generate a **unique answer per question**, grounded strictly in provided data.

- **TemplateAgent**  
  Assembles final JSON pages using predefined templates.

- **SerializationAgent**  
  Writes machine-readable output files to disk.

---

## 📦 Output

Generated files (JSON):
- `faq.json`
- `product_page.json`
- `comparison_page.json`

Each file is structured, deterministic, and suitable for downstream systems.

---



