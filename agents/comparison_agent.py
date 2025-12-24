from typing import Dict, List


class ComparisonAgent:
    """
    Compares two normalized product objects and produces
    a structured comparison dictionary.
    """

    def compare(self, product_a: Dict, product_b: Dict) -> Dict:
        name_a = product_a.get("product_name", "Product A")
        name_b = product_b.get("product_name", "Product B")

        return {
            "products": {
                "product_a": name_a,
                "product_b": name_b,
            },
            "price_comparison": self._compare_price(product_a, product_b),
            "ingredients_comparison": self._compare_ingredients(
                product_a, product_b
            ),
            "benefits_comparison": self._compare_benefits(
                product_a, product_b
            ),
            "summary": self._comparison_summary(product_a, product_b),
        }

    # -------------------------
    # Comparison Helpers
    # -------------------------

    def _compare_price(self, a: Dict, b: Dict) -> Dict:
        name_a = a.get("product_name", "Product A")
        name_b = b.get("product_name", "Product B")

        price_a = a.get("price")
        price_b = b.get("price")

        cheaper = None
        if isinstance(price_a, (int, float)) and isinstance(price_b, (int, float)):
            cheaper = name_a if price_a < price_b else name_b

        return {
            name_a: price_a,
            name_b: price_b,
            "cheaper_option": cheaper,
        }

    def _compare_ingredients(self, a: Dict, b: Dict) -> Dict:
        name_a = a.get("product_name", "Product A")
        name_b = b.get("product_name", "Product B")

        ingredients_a = a.get("key_ingredients", [])
        ingredients_b = b.get("key_ingredients", [])

        return {
            name_a: ingredients_a,
            name_b: ingredients_b,
            "common_ingredients": list(
                set(ingredients_a).intersection(set(ingredients_b))
            ),
        }

    def _compare_benefits(self, a: Dict, b: Dict) -> Dict:
        name_a = a.get("product_name", "Product A")
        name_b = b.get("product_name", "Product B")

        return {
            name_a: a.get("benefits", []),
            name_b: b.get("benefits", []),
        }

    def _comparison_summary(self, a: Dict, b: Dict) -> str:
        name_a = a.get("product_name", "Product A")
        name_b = b.get("product_name", "Product B")

        benefits_a = ", ".join(a.get("benefits", []))
        benefits_b = ", ".join(b.get("benefits", []))

        return (
            f"{name_a} focuses on {benefits_a}, "
            f"while {name_b} offers {benefits_b}."
        )
