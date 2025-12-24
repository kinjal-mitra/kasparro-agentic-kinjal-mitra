""" Serialization Agent

Responsibility:
- Persist final rendered pages to disk as JSON
- Owns file-system interaction
- NO content generation
- NO templating
- NO LLM usage

Inputs:
- page_type (str)
- page_content (dict)
- output_dir (str, optional)

Outputs:
- file_path (str)
"""


import json
from pathlib import Path
from typing import Dict


class SerializationAgent:

    def __init__(self, output_dir: str = "data/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def write_faq_page(self, faq_page: Dict) -> None:
        """
        Writes faq.json
        """
        self._write_json(
            data=faq_page,
            filename="faq.json"
        )

    def write_product_page(self, product_page: Dict) -> None:
        """
        Writes product_page.json
        """
        self._write_json(
            data=product_page,
            filename="product_page.json"
        )

    def write_comparison_page(self, comparison_page: Dict) -> None:
        """
        Writes comparison_page.json
        """
        self._write_json(
            data=comparison_page,
            filename="comparison_page.json"
        )

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _write_json(self, data: Dict, filename: str) -> None:
        """
        Writes a dictionary as formatted JSON to the output directory.
        """

        if not isinstance(data, dict):
            raise ValueError("Serialized data must be a dictionary")

        file_path = self.output_dir / filename

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

