from typing import Dict, List
import json


class QuestionGenerationAgent:
    """
    Generates categorized user questions.

    This agent:
    - DOES generate questions
    - DOES NOT answer them
    - DOES NOT add product facts
    - DOES NOT perform templating
    """

    CATEGORIES = [
        "informational",
        "usage",
        "safety",
        "ingredients",
        "pricing",
        "comparison",
    ]

    MIN_QUESTIONS_PER_CATEGORY = 3

    def __init__(self, llm_client=None):
        """
        llm_client: Optional LLM client.
        If provided, used only for additive expansion.
        """
        self.llm_client = llm_client

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, product: Dict) -> List[Dict]:
        """
        Returns a flat list of:
        [
          { "category": str, "question": str }
        ]
        """
        base_questions = self._generate_rule_based_questions(product)

        if self.llm_client:
            llm_questions = self._generate_llm_questions(product)
            base_questions = self._merge_questions(base_questions, llm_questions)

        self._validate_output(base_questions)

        return self._flatten_questions(base_questions)

    # ------------------------------------------------------------------
    # Rule-Based Generation (Deterministic)
    # ------------------------------------------------------------------

    def _generate_rule_based_questions(self, product: Dict) -> Dict[str, List[str]]:
        name = product.get("product_name", "this product")

        return {
            "informational": [
                f"What is {name}?",
                f"What are the main benefits of {name}?",
                f"Who is {name} suitable for?",
            ],
            "usage": [
                f"How should {name} be used?",
                f"When should {name} be applied?",
                f"How often can {name} be used?",
            ],
            "safety": [
                f"Is {name} safe to use?",
                f"Are there any side effects of {name}?",
                f"Is {name} suitable for sensitive skin?",
            ],
            "ingredients": [
                f"What ingredients are used in {name}?",
                f"Does {name} contain active ingredients?",
                f"What is the concentration of key ingredients in {name}?",
            ],
            "pricing": [
                f"What is the price of {name}?",
                f"Is {name} affordable?",
                f"Does {name} offer good value for money?",
            ],
            "comparison": [
                f"How does {name} compare to similar products?",
                f"What makes {name} different from alternatives?",
                f"Is {name} better than competing products?",
            ],
        }

    # ------------------------------------------------------------------
    # Optional LLM Expansion (Additive Only)
    # ------------------------------------------------------------------

    def _generate_llm_questions(self, product: Dict) -> Dict[str, List[str]]:
        prompt = self._build_llm_prompt(product)
        raw = self.llm_client.generate(prompt)

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        return {}

    def _build_llm_prompt(self, product: Dict) -> str:
        return f"""
                You are generating additional user questions.

                Rules:
                - Use ONLY the provided product data
                - Do NOT add new facts
                - Do NOT answer the questions
                - Output STRICT JSON
                - Keys must be exactly: {self.CATEGORIES}

                Product Data:
                {json.dumps(product, indent=2)}

                Output format:
                {{
                "informational": [string],
                "usage": [string],
                "safety": [string],
                "ingredients": [string],
                "pricing": [string],
                "comparison": [string]
                }}
                """.strip()

    # ------------------------------------------------------------------
    # Merge & Validation
    # ------------------------------------------------------------------

    def _merge_questions(
        self,
        base: Dict[str, List[str]],
        extra: Dict[str, List[str]],
    ) -> Dict[str, List[str]]:

        for category in self.CATEGORIES:
            if category in extra and isinstance(extra[category], list):
                base[category].extend(extra[category])

        # Deduplicate
        for category, questions in base.items():
            seen = set()
            base[category] = [
                q for q in questions
                if not (q in seen or seen.add(q))
            ]

        return base

    def _validate_output(self, questions: Dict[str, List[str]]) -> None:
        for category in self.CATEGORIES:
            if category not in questions:
                raise ValueError(f"Missing category: {category}")

            if len(questions[category]) < self.MIN_QUESTIONS_PER_CATEGORY:
                raise ValueError(
                    f"Category '{category}' has fewer than "
                    f"{self.MIN_QUESTIONS_PER_CATEGORY} questions"
                )

            for q in questions[category]:
                if not isinstance(q, str) or "?" not in q:
                    raise ValueError(
                        f"Invalid question in '{category}': {q}"
                    )

    # ------------------------------------------------------------------
    # Flatten for Pipeline Consumption
    # ------------------------------------------------------------------

    def _flatten_questions(self, questions: Dict[str, List[str]]) -> List[Dict]:
        return [
            {"category": category, "question": q}
            for category, qs in questions.items()
            for q in qs
        ]
