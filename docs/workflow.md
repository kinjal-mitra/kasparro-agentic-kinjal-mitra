# Workflow & Agent Mapping

This document defines **how agents are mapped to orchestration nodes** and how data flows
through the system at an execution level.

---

## Agent → Node Mapping

| Node ID | Agent Class | Responsibility | Inputs | Outputs |
|-------|-------------|----------------|--------|---------|
| Input | — | Product data source | product_data.json | Raw product data |
| Parser | ParserAgent | Normalize & validate product data | Raw JSON | Normalized product |
| Questions | QuestionGenerationAgent | Generate categorized user questions | Product object | Question list |
| Logic | ContentLogicAgent | Apply reusable content logic blocks | Product + questions | Structured blocks |
| Compare | ComparisonAgent | Compare Product A vs Product B | Product objects | Comparison facts |
| TemplateFAQ | TemplateAgent (FAQ) | Assemble FAQ page | Logic blocks | faq.json |
| TemplatePages | TemplateAgent (Pages) | Assemble product & comparison pages | Logic + comparison | Page JSON |
| Serialize | SerializationAgent | Persist outputs to disk | Page JSON | Final JSON files |

---

## Data Flow Summary

1. Product input is parsed and normalized.
2. Questions, logic blocks, and comparison data are generated independently.
3. Template agents assemble page-level JSON.
4. Serialization agent writes machine-readable outputs.
