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
    def __init__(self, use_llm: bool = True):
        self.llm_client = LLMClient() if use_llm else None

        self.parser_agent = ParserAgent()
        self.question_agent = QuestionGenerationAgent(
            llm_client=self.llm_client
        )
        self.content_logic_agent = ContentLogicAgent(
            llm_client=self.llm_client
        )
        self.comparison_agent = ComparisonAgent()

        self.template_agent = TemplateAgent()
        self.serialization_agent = SerializationAgent()

    def run(self, raw_product_data: dict) -> dict:
        normalized_product = self.parser_agent.parse(raw_product_data)

        questions = self.question_agent.generate(normalized_product)

        product_blocks = self.content_logic_agent.generate(
            content_type="product_page",
            payload=normalized_product,
        )

        faq_blocks = self.content_logic_agent.generate(
            content_type="faq",
            payload={
                "product": normalized_product,
                "questions": questions,
            },
        )

        comparison_blocks = self.comparison_agent.compare(
            product_a=normalized_product,
            product_b=self._build_fictional_product(),
        )

        product_page = self.template_agent.render(
            content_type="product_page",
            structured_blocks=product_blocks,
        )

        faq_page = self.template_agent.render(
            content_type="faq",
            structured_blocks=faq_blocks,
        )

        comparison_page = self.template_agent.render(
            content_type="comparison",
            structured_blocks=comparison_blocks,
        )

        return {
            "product_page": self.serialization_agent.serialize(
                page_type="product_page",
                page_content=product_page,
            ),
            "faq": self.serialization_agent.serialize(
                page_type="faq",
                page_content=faq_page,
            ),
            "comparison": self.serialization_agent.serialize(
                page_type="comparison",
                page_content=comparison_page,
            ),
        }

    def _build_fictional_product(self) -> dict:
        return {
            "name": "RadiantPlus Vitamin C Serum",
            "concentration": "8% Vitamin C",
            "skin_type": ["Dry", "Normal"],
            "ingredients": ["Vitamin C", "Niacinamide"],
            "benefits": ["Hydration", "Glow"],
            "usage": "Apply at night after cleansing",
            "price": 799,
        }
