from pathlib import Path
import json

from graph.graph import build_graph
from graph.state import AgentState
from agents.serialization_agent import SerializationAgent


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"

    raw_product_a = load_json(data_dir / "input" / "product_data.json")
    raw_product_b = load_json(data_dir / "input" / "fictitious_product.json")

    # -------------------------
    # Initialize state
    # -------------------------
    initial_state = AgentState(
        raw_product_a=raw_product_a,
        raw_product_b=raw_product_b,
    )

    # -------------------------
    # Run LangGraph
    # -------------------------
    graph = build_graph()
    final_state = graph.invoke(initial_state)

    # -------------------------
    # Serialize outputs (post-graph)
    # -------------------------
    serializer = SerializationAgent(output_dir=data_dir / "output")

    serializer.write_faq_page(final_state["faq_page"])
    serializer.write_product_page(final_state["product_page"])
    serializer.write_comparison_page(final_state["comparison_page"])

    # -------------------------
    # Save execution log
    # -------------------------
    log_path = data_dir / "output" / "execution_log.txt"

    with log_path.open("w", encoding="utf-8") as f:
        for entry in final_state["execution_log"]:
            f.write(entry + "\n")

    print(f"\n Execution log saved to: {log_path}")



    print("LangGraph pipeline executed successfully")


if __name__ == "__main__":
    main()
