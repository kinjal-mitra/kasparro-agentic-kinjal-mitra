# Project Documentation  
## Kasparro – Multi-Agent Content Generation System

---

## Problem Statement

Design and implement a modular agentic system that automatically converts structured product data into multiple machine-readable content pages, without relying on a monolithic LLM script.

The focus is on **system design, orchestration, and agent responsibilities**, not domain expertise or content writing.

---

## Expected Inputs

- A structured JSON-like product dataset containing:
  - Product name
  - Ingredients
  - Benefits
  - Usage instructions
  - Safety information
  - Price

This dataset is the **only source of truth** used by the system.

---

## Expected Outputs

The system generates the following **machine-readable JSON outputs**:

- FAQ Page (question–answer pairs)
- Product Description Page
- Comparison Page (vs a fictional product)

All outputs are deterministic in structure and suitable for downstream systems.

---

## Solution Overview

The solution is implemented as a **multi-agent pipeline**, where each agent has a single responsibility and communicates via explicit data contracts.

The Large Language Model (LLM) is used **only where reasoning and natural language synthesis are required**, and never as a monolithic content generator.

---

## System Design (Core Section)

### 1. High-Level Architecture

```
+------------------+
|  Raw Product     |
|     Data         |
+--------+---------+
         |
         v
+------------------+
|   ParserAgent    |
| (Normalization)  |
+--------+---------+
         |
         v
+--------------------------+
| QuestionGenerationAgent  |
| (What should users ask?) |
+--------+-----------------+
         |
         v
+------------------------------------+
|   For Each Generated Question      |
+----------------+-------------------+
                 |
                 v
      +------------------------+
      |  ContentLogicAgent     |
      |  (Facts Only Context)  |
      +-----------+------------+
                  |
                  v
      +------------------------+
      | AnswerGenerationAgent  |
      | (LLM – One Q, One A)   |
      +-----------+------------+
                  |
                  v
+------------------------+
| ComparisonAgent        |
| (LLM – Two Products,   |
|         One field)     |
+-----------+------------+
          |
          v                  
+--------------------------+
|     TemplateAgent        |
| (Structured JSON Pages)  |
+--------+-----------------+
         |
         v
+--------------------------+
|  SerializationAgent     |
| (Write JSON to Disk)    |
+--------------------------+
```

---

### 2. Detailed Orchestration Flow (FAQ Path)

```
Start
  |
  v
Parse raw product data
  |
  v
Generate categorized questions
  |
  v
FOR EACH QUESTION:
    |
    +--> Extract factual context (ContentLogicAgent)
    |
    +--> Generate answer using LLM (AnswerGenerationAgent)
    |
    +--> Attach answer to question
  |
  v
Assemble FAQ JSON (TemplateAgent)
  |
  v
Write faq.json to disk
  |
 End
```

---

### 3. Agent Responsibilities

**ParserAgent**
```
Raw JSON  -->  Normalized Product Object
```

**QuestionGenerationAgent**
```
Product Data  -->  { category, question }[]
```

**ContentLogicAgent**
```
Product Data + Category  -->  Structured Facts
```

**AnswerGenerationAgent**
```
Facts + Question  -->  Natural Language Answer
```

**TemplateAgent**
```
Q&A Blocks  -->  Final JSON Pages
```

**SerializationAgent**
```
JSON Object  -->  File on Disk
```

**ComparisonAgent**
```
Facts + Product Data (Real + Fictitous)  -->  Natural Language Answer (Comparison Block)
```

---


