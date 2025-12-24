import json
from pathlib import Path

from pipeline import Orchestrator



def load_product_data() -> dict:
    """
    Loads product_data.json using pathlib (OS-agnostic).
    """
    project_root = Path(__file__).resolve().parent
    input_path = project_root / "data" / "input" / "product_data.json"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    """
    Main execution entry.
    """
    raw_product_data = load_product_data()

    orchestrator = Orchestrator(use_llm=True)
    output_paths = orchestrator.run(raw_product_data)

    print("\n✅ Pipeline executed successfully.\n")
    print("Generated files:")
    for page, path in output_paths.items():
        print(f"  - {page}: {path}")


if __name__ == "__main__":
    main()
