from typing import Dict


class ContentLogicAgent:
    """
    Provides structured, category-specific factual context
    extracted from normalized product data.

    This agent:
    - DOES NOT generate natural language
    - DOES NOT call the LLM
    - ONLY returns structured facts
    """

    def build_context(self, product_data: Dict, category: str) -> Dict:
        """
        Build supporting factual context for a given FAQ category.
        """
        category = category.lower()

        handlers = {
            "informational": self._informational_context,
            "usage": self._usage_context,
            "safety": self._safety_context,
            "ingredients": self._ingredients_context,
            "pricing": self._pricing_context,
            "comparison": self._comparison_context,
        }

        handler = handlers.get(category)
        if not handler:
            return {}

        return handler(product_data)

    # -------------------------
    # Context Builders (Facts Only)
    # -------------------------

    def _informational_context(self, product: Dict) -> Dict:
        return {
            "product_name": product.get("product_name"),
            "benefits": product.get("benefits"),
            "skin_type": product.get("skin_type"),
        }

    def _usage_context(self, product: Dict) -> Dict:
        return {
            "how_to_use": product.get("how_to_use"),
        }

    def _safety_context(self, product: Dict) -> Dict:
        return {
            "side_effects": product.get("side_effects"),
            "skin_type": product.get("skin_type"),
        }

    def _ingredients_context(self, product: Dict) -> Dict:
        return {
            "key_ingredients": product.get("key_ingredients"),
            "concentration": product.get("concentration"),
        }

    def _pricing_context(self, product: Dict) -> Dict:
        return {
            "price": product.get("price"),
            "product_name": product.get("product_name"),
        }

    def _comparison_context(self, product: Dict) -> Dict:
        # ComparisonAgent handles actual comparison logic
        return {
            "product_name": product.get("product_name"),
            "price": product.get("price"),
            "key_ingredients": product.get("key_ingredients"),
            "benefits": product.get("benefits"),
        }
