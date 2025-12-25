# Comparison-specific logic and prompt block.


"""
Centralized prompt builders for product comparison.

This module contains ONLY prompt construction logic.
No LLM calls, no parsing.
"""


def build_field_comparison_prompt( section_name: str, field: str,name_a: str, name_b: str, values_a, values_b) -> str:
    """
    Builds a field-specific comparison prompt for Gemini.
    """

    section_instructions = {
        "ingredients_comparison": (
            "Compare formulation focus and ingredient strategy."
        ),
        "benefits_comparison": (
            "Compare user-visible benefits and outcomes."
        ),
        "skin_type_comparison": (
            "Compare suitability for different skin types."
        ),
        "usage_comparison": (
            "Compare ease of use and daily routine compatibility."
        ),
        "side_effects_comparison": (
            "Compare tolerability and potential risks."
        )
    }

    instruction = section_instructions.get(
        section_name, "Compare the two products."
    )

    return f"""
                You are comparing two skincare products.

                Task:
                {instruction}

                Rules:
                - Use ONLY the provided data
                - Do NOT add assumptions
                - Be concise (1–2 sentences)

                {name_a} ({field}):
                {values_a}

                {name_b} ({field}):
                {values_b}
                """


def build_overall_summary_prompt(product_a: dict, product_b: dict) -> str:
    """
    Builds a prompt for generating an overall product comparison summary.
    """

    return f"""
                You are given full details of two skincare products.

                Task:
                Provide a short overall comparison summary highlighting
                key differences and which type of user each product suits best.

                Rules:
                - Use ONLY the provided data
                - No assumptions
                - 2 to 3 sentences maximum

                Product A:
                {product_a}

                Product B:
                {product_b}
                """
