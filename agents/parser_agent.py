import json
from typing import Dict, List

from typing import Dict, List


class ParserAgent:
    """
    Parses raw product input data and converts it into
    a normalized internal product representation.
    """

    REQUIRED_FIELDS = [
        "product_name",
        "concentration",
        "skin_type",
        "key_ingredients",
        "benefits",
        "how_to_use",
        "side_effects",
        "price",
    ]

    # -------------------------
    # Public API
    # -------------------------
    def parse(self, raw_data: Dict) -> Dict:
        """
        Entry point used by orchestrator.
        """
        self._validate(raw_data)
        return self._normalize(raw_data)

    # -------------------------
    # Validation
    # -------------------------
    def _validate(self, data: Dict) -> None:
        missing = [f for f in self.REQUIRED_FIELDS if f not in data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

    # -------------------------
    # Normalization
    # -------------------------
    def _normalize(self, data: Dict) -> Dict:
        return {
            "name": data["product_name"].strip(),
            "concentration": data["concentration"].strip(),
            "skin_type": self._normalize_list(data["skin_type"]),
            "ingredients": self._normalize_list(data["key_ingredients"]),
            "benefits": self._normalize_list(data["benefits"]),
            "usage": data["how_to_use"].strip(),
            "side_effects": data["side_effects"].strip(),
            "price": self._parse_price(data["price"]),
        }

    def _normalize_list(self, value) -> List[str]:
        if isinstance(value, list):
            return [v.strip() for v in value]
        if isinstance(value, str):
            return [v.strip() for v in value.split(",")]
        return []

    def _parse_price(self, price) -> int:
        if isinstance(price, (int, float)):
            return int(price)

        if isinstance(price, str):
            cleaned = (
                price.replace("₹", "")
                .replace(",", "")
                .strip()
            )
            return int(float(cleaned))

        raise ValueError(f"Invalid price format: {price}")

'''
class ParserAgent:
    """
    Parses raw product input data and converts it into
    a normalized internal product representation.
    """

    REQUIRED_FIELDS = [
        "product_name",
        "concentration",
        "skin_type",
        "key_ingredients",
        "benefits",
        "how_to_use",
        "side_effects",
        "price"
    ]
    
    def __init__(self, input_path: str):
        self.input_path = input_path


    def load_raw_data(self) -> Dict:
        with open(self.input_path, "r", encoding="utf-8") as f:
            return json.load(f)


    def validate(self, data: Dict) -> None:
        missing = [f for f in self.REQUIRED_FIELDS if f not in data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        
    def _parse_price(self, price: str) -> int:
        try:
            cleaned = price.replace("₹", "").replace(",", "").strip()
            return int(float(cleaned))
        except Exception:
            raise ValueError(f"Invalid price format: {price}")


    def normalize(self, data: Dict) -> Dict:
        """
        Converts raw data into a consistent internal schema.
        """
        normalized = {
            "name": data["product_name"].strip(),
            "concentration": data["concentration"].strip(),
            "skin_type": self._normalize_list(data["skin_type"]),
            "ingredients": self._normalize_list(data["key_ingredients"]),
            "benefits": self._normalize_list(data["benefits"]),
            "usage": data["how_to_use"].strip(),
            "side_effects": data["side_effects"].strip(),
            "price": {
                "currency": "INR",
                "amount": self._parse_price(data["price"])
            }
        }
        return normalized

    def _normalize_list(self, value) -> List[str]:
        if isinstance(value, list):
            return [v.strip() for v in value]
        if isinstance(value, str):
            return [v.strip() for v in value.split(",")]
        return []

    def run(self) -> Dict:
        raw_data = self.load_raw_data()
        self.validate(raw_data)
        return self.normalize(raw_data)


if __name__ == "__main__":
    agent = ParserAgent("data/input/product_data.json")
    normalized_product = agent.run()

    with open("data/internal/normalized_product.json", "w", encoding="utf-8") as f:
        json.dump(normalized_product, f, indent=2)

    print("✅ Product data normalized successfully.")
'''

