""" Pipeline Module

Responsibility:
- Own the execution graph of the system
- Coordinate agents via dependency injection
- Maintain strict separation of concerns

This Pipeline Module:
- Does NOT load files
- Does NOT contain business logic
- Does NOT contain content logic
- Does NOT do templating
- Delegates persistence to SerializationAgent
"""
from agents.parser_agent import ParserAgent
from agents.question_generation_agent import QuestionGenerationAgent
from agents.content_logic_agent import ContentLogicAgent
from agents.template_agent import TemplateAgent
from agents.serialization_agent import SerializationAgent
from agents.comparison_agent import ComparisonAgent

from llm.llm_client import LLMClient


class Pipeline:
    """
    Orchestrates the multi-agent content generation workflow.
    """

    def __init__(
        self,
        parser_agent,
        question_agent,
        content_logic_agent,
        template_agent,
        comparison_agent
    ):
        self.parser_agent = parser_agent
        self.question_agent = question_agent
        self.content_logic_agent = content_logic_agent
        self.template_agent = template_agent
        self.comparison_agent = comparison_agent

    def run(self, raw_product_data: dict) -> dict:
        normalized_product = self.parser_agent.parse(raw_product_data)

        questions = self.question_agent.generate(normalized_product)

        faq_items = self.content_logic_agent.generate(
            product_data=normalized_product,
            questions=questions
        )

        faq_page = self.template_agent.build_faq_page(faq_items)

        comparison_blocks = self.comparison_agent.compare(
            product_a=normalized_product,
            product_b=self._build_fictional_product()
        )

        comparison_page = self.template_agent.build_comparison_page(
            comparison_blocks
        )

        product_page = self.template_agent.build_product_page(
            normalized_product
        )

        return {
            "faq_page": faq_page,
            "product_page": product_page,
            "comparison_page": comparison_page
        }

    def _build_fictional_product(self) -> dict:
        return {
            "product_name": "RadiantPlus Vitamin C Serum",
            "concentration": "8% Vitamin C",
            "skin_type": ["Dry", "Normal"],
            "key_ingredients": ["Vitamin C", "Niacinamide"],
            "benefits": ["Hydration", "Glow"],
            "how_to_use": "Apply at night after cleansing",
            "price": 799,
        }


