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

# Optional LLM client (shared dependency)
from llm.llm_client import LLMClient


class Orchestrator:
    def __init__(self, use_llm: bool = True):
        """
        Initialize shared dependencies and agents.

        Args:
            use_llm (bool): Whether to enable LLM-backed agents
        """

        # -------------------------
        # Shared Dependencies
        # -------------------------
        self.llm_client = LLMClient() if use_llm else None

        # -------------------------
        # Agents (pure & injected)
        # -------------------------
        self.parser_agent = ParserAgent()

        self.question_agent = QuestionGenerationAgent(
            llm_client=self.llm_client
        )

        self.content_logic_agent = ContentLogicAgent(
            llm_client=self.llm_client
        )

        self.template_agent = TemplateAgent()
        self.serialization_agent = SerializationAgent()

    # -------------------------
    # Pipeline Execution
    # -------------------------
    def run(self, raw_product_data: dict) -> dict:
        """
        Executes the full agentic pipeline.

        Args:
            raw_product_data (dict): Raw product input data

        Returns:
            dict: Mapping of page_type -> output file path
        """

        # -------------------------
        # Step 1: Parse & normalize
        # -------------------------
        normalized_product = self.parser_agent.parse(raw_product_data)

        # -------------------------
        # Step 2: Generate questions
        # -------------------------
        questions = self.question_agent.generate(normalized_product)

        # -------------------------
        # Step 3: Generate content blocks
        # -------------------------
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

        comparison_blocks = self.content_logic_agent.generate(
            content_type="comparison",
            payload={
                "product_a": normalized_product,
                "product_b": self._build_fictional_product(),
            },
        )

        # -------------------------
        # Step 4: Render templates
        # -------------------------
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

        # -------------------------
        # Step 5: Serialize outputs
        # -------------------------
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

    # -------------------------
    # Internal Helpers
    # -------------------------
    def _build_fictional_product(self) -> dict:
        """
        Creates a deterministic fictional product
        for comparison purposes.
        """
        return {
            "name": "RadiantPlus Vitamin C Serum",
            "concentration": "8% Vitamin C",
            "skin_type": ["Dry", "Normal"],
            "ingredients": ["Vitamin C", "Niacinamide"],
            "benefits": ["Hydration", "Glow"],
            "usage": "Apply at night after cleansing",
            "price": 799,
        }