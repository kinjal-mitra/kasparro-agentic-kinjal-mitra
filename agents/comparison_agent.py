from typing import Dict, Any

from llm.comparison_llm import ComparisonClient
from logic_blocks.comparison_block import (
    build_field_comparison_prompt,
    build_overall_summary_prompt
)


class ComparisonAgent:
    """
    Compares two normalized products using:
    - Deterministic price comparison
    - Field-wise LLM comparisons with verdicts
    - One final overall LLM summary

    IMPORTANT:
    This agent assumes BOTH products are already normalized
    by ParserAgent.
    """

    LLM_FIELDS = {
        "ingredients_comparison": "ingredients",
        "benefits_comparison": "benefits",
        "skin_type_comparison": "skin_type",
        "usage_comparison": "usage",
        "side_effects_comparison": "side_effects"
    }

    def __init__(self):
        self.llm = ComparisonClient()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compare(self, product_a: Dict, product_b: Dict) -> Dict:
        name_a = product_a.get("name")
        name_b = product_b.get("name")

        if not name_a or not name_b:
            raise ValueError(
                "ComparisonAgent requires normalized products with 'name' field"
            )

        output = {
            "products": {
                "product_a": name_a,
                "product_b": name_b
            },
            "price_comparison": self._compare_price(product_a, product_b)
        }

        # Field-wise LLM comparisons
        for section_name, field in self.LLM_FIELDS.items():
            output[section_name] = self._compare_field(
                section_name=section_name,
                field=field,
                product_a=product_a,
                product_b=product_b
            )

        # Overall summary
        output["summary"] = self._generate_overall_summary(
            product_a, product_b
        )

        return output

    # ------------------------------------------------------------------
    # Price Comparison (Deterministic)
    # ------------------------------------------------------------------

    def _extract_price_amount(self, product: Dict) -> Any:
        """
        Extracts numeric price amount from normalized product.
        """
        price = product.get("price")

        if isinstance(price, dict):
            return price.get("amount")

        return price

    def _compare_price(self, a: Dict, b: Dict) -> Dict:
        name_a = a["name"]
        name_b = b["name"]

        price_a = self._extract_price_amount(a)
        price_b = self._extract_price_amount(b)

        cheaper = None
        if isinstance(price_a, (int, float)) and isinstance(price_b, (int, float)):
            cheaper = name_a if price_a < price_b else name_b

        return {
            name_a: price_a,
            name_b: price_b,
            "cheaper_option": cheaper
        }

    # ------------------------------------------------------------------
    # Field Comparison (LLM-powered)
    # ------------------------------------------------------------------

    def _compare_field(
        self,
        section_name: str,
        field: str,
        product_a: Dict,
        product_b: Dict
    ) -> Dict:
        name_a = product_a["name"]
        name_b = product_b["name"]

        values_a = product_a.get(field)
        values_b = product_b.get(field)

        # Normalize empty values explicitly
        values_a = values_a if values_a is not None else []
        values_b = values_b if values_b is not None else []

        prompt = build_field_comparison_prompt(
            section_name=section_name,
            field=field,
            name_a=name_a,
            name_b=name_b,
            values_a=values_a,
            values_b=values_b
        )

        verdict = self.llm.generate(prompt)

        return {
            name_a: values_a,
            name_b: values_b,
            "verdict": verdict
        }

    # ------------------------------------------------------------------
    # Overall Summary (LLM-powered)
    # ------------------------------------------------------------------

    def _generate_overall_summary(
        self,
        product_a: Dict,
        product_b: Dict
    ) -> str:
        prompt = build_overall_summary_prompt(
            product_a, product_b
        )

        return self.llm.generate(prompt)
