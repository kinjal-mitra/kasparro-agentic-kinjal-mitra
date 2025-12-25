"""
Pipeline Module

Responsibility:
- Own the execution graph of the system
- Coordinate agents via dependency injection
- Maintain strict separation of concerns

This Pipeline Module:
- Does NOT load files
- Does NOT construct data
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
from agents.answer_generation_agent import AnswerGenerationAgent


class Pipeline:
    """
    Orchestrates the multi-agent content generation workflow.
    """

    def __init__(
        self,
        parser_agent: ParserAgent,
        question_agent: QuestionGenerationAgent,
        content_logic_agent: ContentLogicAgent,
        answer_generation_agent: AnswerGenerationAgent,
        template_agent: TemplateAgent,
        comparison_agent: ComparisonAgent,
    ):
        self.parser_agent = parser_agent
        self.question_agent = question_agent
        self.content_logic_agent = content_logic_agent
        self.answer_generation_agent = answer_generation_agent
        self.template_agent = template_agent
        self.comparison_agent = comparison_agent

    def run(
        self,
        raw_product_data: dict,
        raw_comparison_product_data: dict
    ) -> dict:
        """
        Execute the full content generation pipeline.

        Parameters
        ----------
        raw_product_data : dict
            Raw input product data (primary product)

        raw_comparison_product_data : dict
            Raw input product data (fictitious / comparison product)

        Returns
        -------
        dict
            Generated FAQ, Product Page, and Comparison Page
        """

        # -------------------------
        # Parse & Normalize Inputs
        # -------------------------
        normalized_product = self.parser_agent.parse(raw_product_data)
        normalized_comparison_product = self.parser_agent.parse(
            raw_comparison_product_data
        )

        # -------------------------
        # FAQ Generation
        # -------------------------
        questions = self.question_agent.generate(normalized_product)

        faq_items = []
        for q in questions:
            supporting_context = self.content_logic_agent.build_context(
                product_data=normalized_product,
                category=q["category"]
            )

            faq_item = self.answer_generation_agent.generate_answer(
                product=normalized_product,
                category=q["category"],
                question=q["question"],
                supporting_context=supporting_context
            )

            faq_items.append({
                "category": q["category"],
                "question": faq_item["question"],
                "answer": faq_item["answer"]
            })

        faq_page = self.template_agent.build_faq_page(faq_items)

        # -------------------------
        # Product Page
        # -------------------------
        product_page = self.template_agent.build_product_page(
            normalized_product
        )

        # -------------------------
        # Comparison Page
        # -------------------------
        comparison_blocks = self.comparison_agent.compare(
            product_a=normalized_product,
            product_b=normalized_comparison_product
        )

        comparison_page = self.template_agent.build_comparison_page(
            comparison_blocks
        )

        # -------------------------
        # Final Output
        # -------------------------
        return {
            "faq_page": faq_page,
            "product_page": product_page,
            "comparison_page": comparison_page
        }
