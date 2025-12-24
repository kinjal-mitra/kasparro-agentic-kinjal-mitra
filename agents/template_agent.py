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


class TemplateAgent:
    def render(self, content_type: str, structured_blocks: dict) -> dict:
        """
        Entry point for rendering templates
        """
        if content_type == "product_page":
            return self._render_product_page(structured_blocks)

        if content_type == "faq":
            return self._render_faq_page(structured_blocks)

        if content_type == "comparison":
            return self._render_comparison_page(structured_blocks)

        raise ValueError(f"Unsupported content_type: {content_type}")

    # -------------------------
    # Product Page Template
    # -------------------------
    def _render_product_page(self, blocks: dict) -> dict:
        return {
            "page_type": "product_page",
            "product_overview": blocks["overview"],
            "ingredients_section": blocks["ingredients"],
            "benefits_section": blocks["benefits"],
            "usage_section": blocks["usage"],
            "pricing_section": blocks["pricing"],
            "safety_section": blocks["safety"],
            "skin_type_section": blocks["skin_type"],
        }

    # -------------------------
    # FAQ Page Template
    # -------------------------
    def _render_faq_page(self, blocks: dict) -> dict:
        return {
            "page_type": "faq",
            "total_questions": blocks["faq_count"],
            "questions": blocks["faqs"],
        }

    # -------------------------
    # Comparison Page Template
    # -------------------------
    def _render_comparison_page(self, blocks: dict) -> dict:
        return {
            "page_type": "comparison",
            "products_compared": blocks["products"],
            "price_comparison": blocks["price_comparison"],
            "ingredients_comparison": blocks["ingredients_comparison"],
            "benefits_comparison": blocks["benefits_comparison"],
            "summary": blocks["summary"],
        }
