""" Content Logic Agent
Responsibility:
- Transform normalized product data into structured content blocks
- Apply deterministic rules (and optional LLM assistance)
- Produce machine-readable content fragments
- NO file I/O
- NO templates
- NO orchestration logic

Inputs:
- normalized_product (dict)
- content_type (str)
- optional context (comparison product, question list, etc.)

Outputs:
- structured dict blocks ready for template_agent
"""

from typing import Dict, List

class ContentLogicAgent:
    """
    Content Logic Agent

    Responsibilities:
    - Accepts generated questions with categories
    - Routes each question to the correct logic block
    - Generates deterministic answers using product data
    - Produces Q&A objects for downstream templating

    This agent:
    - Does NOT generate questions
    - Does NOT perform templating
    - Does NOT add new product facts
    """

    def __init__(self):
        self.logic_blocks = {
            "informational": self._informational_block,
            "usage": self._usage_block,
            "safety": self._safety_block,
            "ingredients": self._ingredients_block,
            "pricing": self._pricing_block,
            "comparison": self._comparison_block
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        product_data: Dict,
        questions: List[Dict]
    ) -> List[Dict]:
        """
        Input:
        - product_data (dict)
        - questions: List[{ category, question }]

        Output:
        - List[{ category, question, answer }]
        """

        answered_questions = []

        for item in questions:
            category = item.get("category")
            question_text = item.get("question")

            if category not in self.logic_blocks:
                raise ValueError(f"Unsupported category: {category}")

            answer = self.logic_blocks[category](product_data)

            answered_questions.append({
                "category": category,
                "question": question_text,
                "answer": answer
            })

        return answered_questions

    # ------------------------------------------------------------------
    # Logic Blocks (Deterministic, Rule-Based)
    # ------------------------------------------------------------------

    def _informational_block(self, product: Dict) -> str:
        return (
            f"{product['name']} is a skincare serum containing "
            f"{product['concentration']} Vitamin C. It is designed for "
            f"{', '.join(product['skin_type'])} skin types and helps with "
            f"{', '.join(product['benefits']).lower()}."
        )

    def _usage_block(self, product: Dict) -> str:
        return product["usage"]

    def _safety_block(self, product: Dict) -> str:
        side_effects = product.get("side_effects")
        if side_effects:
            return (
                f"The product is generally safe to use. "
                f"However, {side_effects.lower()}."
            )
        return "The product is generally safe to use."

    def _ingredients_block(self, product: Dict) -> str:
        ingredients = ", ".join(product["ingredients"])
        return f"The key ingredients in this product are {ingredients}."

    def _pricing_block(self, product: Dict) -> str:
        return f"The price of the product is {product['price']}."

    def _comparison_block(self, product: Dict) -> str:
        return (
            "A direct comparison cannot be made because details of other "
            "products are not available. This product contains "
            f"{product['concentration']} Vitamin C and is priced at "
            f"{product['price']}."
        )
