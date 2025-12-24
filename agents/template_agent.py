""" Template Agent
Responsibility:
- Convert structured content blocks into final page JSONs
- Owns page schemas and field layout
- NO business logic
- NO LLM usage
- NO file I/O
- Deterministic formatting only

Inputs:
- content_type (str)
- structured_blocks (dict)

Outputs:
- final_page_json (dict)
"""


from typing import Dict, List


class TemplateAgent:
    """
    Template Agent

    Responsibilities:
    - Assemble final machine-readable JSON pages
    - Apply page-level structure and metadata
    - Remain completely content-agnostic

    This agent:
    - Does NOT generate questions
    - Does NOT generate answers
    - Does NOT apply business logic
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_faq_page(self, qa_items: List[Dict]) -> Dict:
        """
        Builds FAQ page JSON.

        Input:
        - qa_items: List[{ category, question, answer }]

        Output:
        - faq.json compatible structure
        """

        self._validate_qa_items(qa_items)

        return {
            "page_type": "faq",
            "total_questions": len(qa_items),
            "questions": [
                {
                    "category": item["category"],
                    "question": item["question"],
                    "answer": item["answer"]
                }
                for item in qa_items
            ]
        }

    def build_product_page(self, product_blocks: Dict) -> Dict:
        """
        Builds Product Description page JSON.

        Input:
        - product_blocks (dict): precomputed content blocks

        Output:
        - product_page.json structure
        """

        return {
            "page_type": "product",
            "content": product_blocks
        }

    def build_comparison_page(self, comparison_blocks: Dict) -> Dict:
        """
        Builds Comparison page JSON.

        Input:
        - comparison_blocks (dict)

        Output:
        - comparison_page.json structure
        """

        return {
            "page_type": "comparison",
            "comparison": comparison_blocks
        }

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_qa_items(self, qa_items: List[Dict]) -> None:
        """
        Ensures FAQ entries conform to required schema.
        """

        if not isinstance(qa_items, list):
            raise ValueError("qa_items must be a list")

        for item in qa_items:
            if not isinstance(item, dict):
                raise ValueError("Each QA item must be a dictionary")

            for key in ("category", "question", "answer"):
                if key not in item:
                    raise ValueError(f"Missing key '{key}' in QA item")

            if not isinstance(item["question"], str) or not item["question"].strip():
                raise ValueError("Question must be a non-empty string")

            if not isinstance(item["answer"], str) or not item["answer"].strip():
                raise ValueError("Answer must be a non-empty string")
