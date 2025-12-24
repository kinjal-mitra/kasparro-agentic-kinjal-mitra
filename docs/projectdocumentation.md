# Project Documentation

**Kasparro – AI Agentic Content Generation System**

---

## Problem Statement

Product content generation (FAQs, product pages, and product comparisons) is repetitive, rule-heavy, and difficult to scale consistently without clear system boundaries.
This project demonstrates a **modular, agent-based automation system** that transforms raw product data into structured, machine-readable content using clearly defined agents and orchestration logic.

The focus of this project is on **system design, agent responsibilities, and data flow**, rather than domain expertise or UI presentation.

---

## Expected Inputs

* Raw product data provided as structured JSON.
* Mandatory product attributes:

  * Product name
  * Concentration or specification
  * Skin type compatibility
  * Key ingredients
  * Benefits
  * Usage instructions
  * Safety or side-effect information
  * Price
* No external data sources or enrichment are used.
* An internally constructed fictional product may be used strictly for comparison purposes.

---

## Expected Outputs

The system generates **three independent, machine-readable JSON outputs**:

1. **FAQ Page (`faq.json`)**

   * Categorized user questions
   * Deterministic, rule-based answers
   * Optional LLM-backed variation without introducing new facts

2. **Product Page (`product_page.json`)**

   * Product overview
   * Ingredients
   * Benefits
   * Usage instructions
   * Pricing details
   * Safety information
   * Skin-type suitability

3. **Comparison Page (`comparison_page.json`)**

   * Side-by-side comparison of two products
   * Price comparison
   * Ingredient overlap
   * Benefit comparison
   * Rule-based summary

All outputs are:

* Structured
* Deterministic
* Schema-consistent
* Suitable for CMS platforms, APIs, and downstream automation pipelines

---

## High-Level System Flow

```
Raw Product Data
      ↓
ParserAgent
      ↓
QuestionGenerationAgent
      ↓
ContentLogicAgent (Product Page + FAQ only)
      ↓
ComparisonAgent (Comparison only)
      ↓
TemplateAgent
      ↓
SerializationAgent
      ↓
JSON Outputs
```

---

## Agent Responsibilities

### 1. ParserAgent

* Validates required fields in raw input data
* Cleans and normalizes product information
* Produces a standardized internal product representation
* Does not perform content generation or formatting

---

### 2. QuestionGenerationAgent

* Generates categorized user questions, including:

  * Informational
  * Usage
  * Safety
  * Ingredients
  * Pricing
  * Comparison
* Guarantees minimum question coverage per category
* Optionally enhances question diversity using an injected LLM
* Does **not** answer questions or add product facts

---

### 3. ContentLogicAgent

* Generates structured **content blocks** for:

  * Product pages
  * FAQ pages
* Applies deterministic, rule-based transformations
* Does **not** perform product comparisons
* Does **not** render templates or serialize output

---

### 4. ComparisonAgent

* Sole owner of all **product comparison logic**
* Compares products based on:

  * Pricing
  * Ingredients
  * Benefits
* Produces a structured comparison object
* Contains no templating, serialization, or orchestration logic

---

### 5. TemplateAgent

* Converts structured content blocks into finalized page layouts
* Applies page-specific templates for:

  * Product pages
  * FAQ pages
  * Comparison pages
* Does not infer, modify, or enrich data

---

### 6. SerializationAgent

* Writes finalized pages to disk as JSON files
* Handles output directory creation
* Ensures clean, machine-readable formatting
* Does not perform content logic or validation

---

## Orchestration Strategy

* The system is coordinated by a central **Orchestrator**.
* Each agent:

  * Has a single, well-defined responsibility
  * Exposes clear input and output contracts
  * Operates without shared global state
* The orchestrator manages:

  * Execution order
  * Dependency injection (e.g., optional LLM client)
  * Data flow between agents

This orchestration approach ensures:

* Modularity
* Testability
* Extensibility
* Clear separation of concerns

---

## Scope and Assumptions

* The system operates strictly on provided input data.
* No external knowledge or enrichment is introduced.
* Content quality is driven by structure and logic rather than creative writing.
* The system is designed for backend automation, not UI rendering.

---

## Conclusion

This project demonstrates a **production-style agentic automation system** with clearly separated responsibilities across parsing, question generation, content logic, comparison, templating, and serialization.
The architecture emphasizes correctness, extensibility, and clarity—closely reflecting real-world AI-driven content generation pipelines used in scalable systems.
