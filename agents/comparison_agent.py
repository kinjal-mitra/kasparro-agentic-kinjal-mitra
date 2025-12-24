from typing import Dict, List


class ComparisonAgent:
    """
    Compares two normalized product objects and produces
    a structured comparison dictionary.
    """

    def compare(self, product_a: Dict, product_b: Dict) -> Dict:
        return {
            "products": {
                "product_a": product_a["name"],
                "product_b": product_b["name"],
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
        return {
            a["name"]: a["price"],
            b["name"]: b["price"],
            "cheaper_option": (
                a["name"] if a["price"] < b["price"] else b["name"]
            ),
        }

    def _compare_ingredients(self, a: Dict, b: Dict) -> Dict:
        return {
            a["name"]: a["ingredients"],
            b["name"]: b["ingredients"],
            "common_ingredients": list(
                set(a["ingredients"]).intersection(set(b["ingredients"]))
            ),
        }

    def _compare_benefits(self, a: Dict, b: Dict) -> Dict:
        return {
            a["name"]: a["benefits"],
            b["name"]: b["benefits"],
        }

    def _comparison_summary(self, a: Dict, b: Dict) -> str:
        return (
            f"{a['name']} focuses on {', '.join(a['benefits'])}, "
            f"while {b['name']} offers {', '.join(b['benefits'])}."
        )
