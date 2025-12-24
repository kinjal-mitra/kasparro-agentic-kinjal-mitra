import json
from pathlib import Path

from agents.parser_agent import ParserAgent
from agents.question_generation_agent import QuestionGenerationAgent
from agents.content_logic_agent import ContentLogicAgent
from agents.template_agent import TemplateAgent
from agents.serialization_agent import SerializationAgent
from agents.comparison_agent import ComparisonAgent
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

    input_path = data_dir / "input" / "product_data.json"
    output_dir = data_dir / "output"

    # ------------------------------------------------------------------
    # Load raw product data
    # ------------------------------------------------------------------
    raw_product_data = load_json(input_path)

    # ------------------------------------------------------------------
    # Instantiate agents
    # ------------------------------------------------------------------
    parser_agent = ParserAgent()
    question_agent = QuestionGenerationAgent()
    content_logic_agent = ContentLogicAgent()
    template_agent = TemplateAgent()
    serialization_agent = SerializationAgent(output_dir=output_dir)
    comparison_agent = ComparisonAgent()

    # ------------------------------------------------------------------
    # Build pipeline
    # ------------------------------------------------------------------
    pipeline = Pipeline(
        parser_agent=parser_agent,
        question_agent=question_agent,
        content_logic_agent=content_logic_agent,
        template_agent=template_agent,
        comparison_agent=comparison_agent
    )

    # ------------------------------------------------------------------
    # Run pipeline
    # ------------------------------------------------------------------
    pages = pipeline.run(raw_product_data)

    # ------------------------------------------------------------------
    # Serialize outputs
    # ------------------------------------------------------------------
    serialization_agent.write_faq_page(pages["faq_page"])

    # (Optional future extensions)
    # serialization_agent.write_product_page(pages["product_page"])
    # serialization_agent.write_comparison_page(pages["comparison_page"])

    print("✅ Content generation pipeline completed successfully.")


if __name__ == "__main__":
    main()
