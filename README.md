# Kasparro – Multi-Agent Content Generation System

This repository implements a **modular, agentic automation system** that transforms structured product data into fully generated, machine-readable content pages.

The system is designed as part of the **Kasparro – Applied AI Engineer Challenge**, with a strong emphasis on **agent boundaries, orchestration, and extensibility** rather than prompt engineering or copywriting.

---

## 🎯 Objective

Automatically generate structured content pages from a small product dataset using a **multi-agent pipeline**, without relying on a monolithic LLM script.

The system produces:
- FAQ Page (question-aware, LLM-generated answers)
- Product Description Page
- Comparison Page (against a fictional product)

All outputs are generated as **clean JSON files**.

---

## 🧠 Core Design Principles

- **Single-responsibility agents**
- **Explicit input/output contracts**
- **LLM usage isolated to one agent**
- **No hidden global state**
- **Deterministic + extensible workflow**

This is a **systems design challenge**, not a content-writing exercise.

---

## 🧩 High-Level Architecture

```
ParserAgent
   ↓
QuestionGenerationAgent
   ↓
ContentLogicAgent  (facts only)
   ↓
AnswerGenerationAgent (LLM)
   ↓
TemplateAgent
   ↓
SerializationAgent
```

Comparison logic runs in parallel using a dedicated `ComparisonAgent`.

---

## 🤖 Key Agents

- **ParserAgent**  
  Normalizes raw product input into an internal schema.

- **QuestionGenerationAgent**  
  Generates categorized, human-readable user questions (rule-based + optional LLM expansion).

- **ContentLogicAgent**  
  Extracts structured, category-specific factual context from product data.

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

## 🚀 How to Run

1. Place product data in:
   ```
   data/input/product_data.json
   ```

2. Run:
   ```bash
   python runner.py
   ```

3. Outputs will be written to:
   ```
   data/output/
   ```

---

## 🧠 Final Note

This repository prioritizes **engineering clarity and system correctness** over surface-level content quality — exactly as expected in real-world agentic systems.
