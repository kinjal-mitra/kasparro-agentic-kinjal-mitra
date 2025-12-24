# Project Documentation  
**Kasparro AI Agentic Content Generation System**

## Problem Statement
Modern product content creation (FAQs, product pages, and comparisons) is repetitive, time-consuming, and difficult to scale consistently. This project automates structured, high-quality content generation from raw product data using a modular, agent-based AI workflow.

## Expected Inputs
- Raw product data in structured or semi-structured formats (e.g., JSON).
- Core product attributes such as:
  - Product name and category  
  - Specifications and features  
  - Pricing information  
  - Ingredients or components  
  - Usage instructions  
  - Safety-related information  
- Optional metadata for content customization (target audience, tone, region, or platform).

## Expected Outputs
- **FAQ Content** derived from product understanding and user intent.
- **Product Page Content** including benefits, usage, safety, pricing, and ingredients.
- **Product Comparison Content** for multiple products.
- All outputs are generated as clean, structured JSON files suitable for:
  - Websites
  - CMS platforms
  - APIs
  - Downstream automation pipelines

## High-Level Flow (Parser → Agents → Output)

### 1. Parser
- Ingests raw product input data.
- Validates, cleans, and normalizes the data into a standardized internal format.

### 2. Agents
- **Question Generation Agent**  
  Generates user-focused questions and FAQs from product attributes.
- **Content Logic Agent**  
  Determines which content blocks apply and how information should be organized.
- **Template Agent**  
  Converts logical content structures into consistent, human-readable formats.
- **Comparison Agent**  
  Produces structured comparisons when multiple products are provided.
- **Serialization Agent**  
  Converts finalized content into output-ready JSON files.

### 3. Output
- Structured content is written to the output directory.
- Generated files are deterministic, reusable, and designed for scalable content automation.
