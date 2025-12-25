import json
from pathlib import Path

from agents.parser_agent import ParserAgent
from agents.question_generation_agent import QuestionGenerationAgent
from agents.content_logic_agent import ContentLogicAgent
from agents.template_agent import TemplateAgent
from agents.serialization_agent import SerializationAgent
from agents.comparison_agent import ComparisonAgent
from agents.answer_generation_agent import AnswerGenerationAgent

from llm.llm_client import LLMClient
from pipeline import Pipeline


def load_json(path: Path) -> dict:
    """
    Load a JSON file safely from disk.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # ------------------------------------------------------------------
    # Resolve paths
    # ------------------------------------------------------------------
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"

    input_dir = data_dir / "input"
    output_dir = data_dir / "output"

    product_a_path = input_dir / "product_data.json"
    product_b_path = input_dir / "fictitious_product.json"

    # ------------------------------------------------------------------
    # Load raw input data
    # ------------------------------------------------------------------
    raw_product_data = load_json(product_a_path)
    raw_fictitious_product_data = load_json(product_b_path)

    # ------------------------------------------------------------------
    # Instantiate agents
    # ------------------------------------------------------------------
    llm_client = LLMClient()

    parser_agent = ParserAgent()
    question_agent = QuestionGenerationAgent()
    content_logic_agent = ContentLogicAgent()
    template_agent = TemplateAgent()
    comparison_agent = ComparisonAgent()
    answer_generation_agent = AnswerGenerationAgent(llm_client)

    serialization_agent = SerializationAgent(output_dir=output_dir)

    # ------------------------------------------------------------------
    # Build pipeline
    # ------------------------------------------------------------------
    pipeline = Pipeline(
        parser_agent=parser_agent,
        question_agent=question_agent,
        content_logic_agent=content_logic_agent,
        answer_generation_agent=answer_generation_agent,
        template_agent=template_agent,
        comparison_agent=comparison_agent
    )

    # ------------------------------------------------------------------
    # Run pipeline
    # ------------------------------------------------------------------
    pages = pipeline.run(
        raw_product_data=raw_product_data,
        raw_comparison_product_data=raw_fictitious_product_data
    )

    # Debug verification
    #print("\n[DEBUG] Generated pages:", pages.keys())
    #print("[DEBUG] comparison_page keys:", pages["comparison_page"].keys())

    # ------------------------------------------------------------------
    # Serialize outputs
    # ------------------------------------------------------------------
    serialization_agent.write_faq_page(pages["faq_page"])
    serialization_agent.write_product_page(pages["product_page"])
    serialization_agent.write_comparison_page(pages["comparison_page"])

    print("\n Content generation pipeline completed successfully.")


if __name__ == "__main__":
    main()
