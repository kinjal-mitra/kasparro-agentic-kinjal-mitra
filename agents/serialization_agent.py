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
import os
from typing import Dict


class SerializationAgent:
    DEFAULT_OUTPUT_DIR = "data/output"

    FILE_MAP = {
        "product_page": "product_page.json",
        "faq": "faq.json",
        "comparison": "comparison_page.json",
    }

    def serialize(
        self,
        page_type: str,
        page_content: Dict,
        output_dir: str | None = None,
    ) -> str:
        """
        Writes page_content to disk as JSON and returns file path
        """

        if page_type not in self.FILE_MAP:
            raise ValueError(f"Unsupported page_type: {page_type}")

        output_dir = output_dir or self.DEFAULT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)

        file_name = self.FILE_MAP[page_type]
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(page_content, f, indent=2, ensure_ascii=False)

        return file_path
