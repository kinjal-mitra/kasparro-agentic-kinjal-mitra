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
from typing import Dict


class ContentLogicAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    # -------------------------
    # Public Entry Point
    # -------------------------
    def generate(self, content_type: str, payload: Dict) -> Dict:
        if content_type == "product_page":
            return self._product_page_blocks(payload)

        if content_type == "faq":
            return self._faq_blocks(payload)

        raise ValueError(f"Unsupported content_type: {content_type}")

    # -------------------------
    # Product Page Logic
    # -------------------------
    def _product_page_blocks(self, product: Dict) -> Dict:
        return {
            "overview": self._overview_block(product),
            "ingredients": self._ingredients_block(product),
            "benefits": self._benefits_block(product),
            "usage": self._usage_block(product),
            "pricing": self._pricing_block(product),
            "safety": self._safety_block(product),
            "skin_type": self._skin_type_block(product),
        }

    def _overview_block(self, product: Dict) -> Dict:
        return {
            "title": product["name"],
            "summary": (
                f"{product['name']} is a {product['concentration']} serum "
                f"designed for {', '.join(product['skin_type'])} skin types."
            ),
        }

    def _ingredients_block(self, product: Dict) -> Dict:
        return {
            "key_ingredients": product["ingredients"],
            "ingredient_count": len(product["ingredients"]),
        }

    def _benefits_block(self, product: Dict) -> Dict:
        return {
            "primary_benefits": product["benefits"],
            "benefit_count": len(product["benefits"]),
        }

    def _usage_block(self, product: Dict) -> Dict:
        return {
            "how_to_use": product["usage"],
            "recommended_time": "Morning",
        }

    def _pricing_block(self, product: Dict) -> Dict:
        return {
            "price": product["price"],
            "currency": "INR",
            "value_positioning": "Mid-range",
        }

    def _safety_block(self, product: Dict) -> Dict:
        return {
            "side_effects": product.get("side_effects", []),
            "disclaimer": "Patch test recommended for sensitive skin.",
        }

    def _skin_type_block(self, product: Dict) -> Dict:
        return {
            "suitable_for": product["skin_type"],
            "not_recommended_for": [],
        }

    # -------------------------
    # FAQ Logic
    # -------------------------
    def _faq_blocks(self, payload: Dict) -> Dict:
        product = payload["product"]
        questions = payload["questions"]

        faqs = []

        for q in questions:
            if isinstance(q, str):
                question_obj = {"question": q, "category": "general"}
            elif isinstance(q, dict):
                question_obj = q
            else:
                raise ValueError(f"Invalid question format: {q}")

            faqs.append(
                {
                    "question": question_obj["question"],
                    "category": question_obj.get("category", "general"),
                    "answer": self._generate_answer(product, question_obj),
                }
            )

        return {
            "faq_count": len(faqs),
            "faqs": faqs,
        }

    def _generate_answer(self, product: Dict, question: Dict) -> str:
        category = question["category"].lower()

        if category == "usage":
            return product["usage"]

        if category == "safety":
            return product.get(
                "side_effects", "No major side effects reported."
            )

        if category == "pricing":
            return f"The product is priced at {product['price']}."

        if category == "ingredients":
            return f"Key ingredients include {', '.join(product['ingredients'])}."

        if self.llm_client:
            prompt = (
                f"Answer the following question using only this product data:\n"
                f"Product: {product}\n"
                f"Question: {question['question']}"
            )
            return self.llm_client.generate(prompt)

        return "Information available on the product page."
