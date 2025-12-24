from typing import Dict, List
import json



class QuestionGenerationAgent:
    """
    Hybrid Question Generation Agent

    Responsibilities:
    - Generate categorized, human-readable user questions
    - Guarantee minimum question coverage deterministically
    - Optionally expand questions using an LLM
    - Enforce strict output schema

    This agent:
    - Does NOT answer questions
    - Does NOT add new product facts
    - Does NOT perform templating
    """

    CATEGORIES = [
        "informational",
        "usage",
        "safety",
        "ingredients",
        "pricing",
        "comparison"
    ]

    MIN_QUESTIONS_PER_CATEGORY = 3

    def __init__(self, llm_client=None):
        """
        llm_client: Optional LLM client.
        If None, the agent runs in rule-only mode.
        """
        self.llm_client = llm_client

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, normalized_product: Dict) -> List[Dict]:
        """
        Generate categorized user questions.

        Output:
        [
          {
            "category": "usage",
            "question": "How should GlowBoost Vitamin C Serum be used?"
          }
        ]
        """

        questions_by_category = self._generate_rule_based_questions(
            normalized_product
        )

        if self.llm_client:
            llm_questions = self._generate_llm_questions(normalized_product)
            questions_by_category = self._merge_questions(
                questions_by_category,
                llm_questions
            )

        self._validate_output(questions_by_category)

        return self._flatten_questions(questions_by_category)

    # ------------------------------------------------------------------
    # Rule-Based Generation (Deterministic Baseline)
    # ------------------------------------------------------------------

    def _generate_rule_based_questions(self, product: Dict) -> Dict[str, List[str]]:
        product_name = product.get("product_name", "this product")

        return {
            "informational": [
                f"What is {product_name}?",
                f"What are the main benefits of {product_name}?",
                f"Who is {product_name} suitable for?"
            ],
            "usage": [
                f"How should {product_name} be used?",
                f"When is the best time to use {product_name}?",
                f"How often should {product_name} be applied?"
            ],
            "safety": [
                f"Is {product_name} safe to use?",
                f"Are there any side effects of {product_name}?",
                f"Is {product_name} suitable for sensitive skin?"
            ],
            "ingredients": [
                f"What ingredients are used in {product_name}?",
                f"What role do the ingredients in {product_name} play?",
                f"Does {product_name} contain active ingredients?"
            ],
            "pricing": [
                f"What is the price of {product_name}?",
                f"Is {product_name} affordable?",
                f"Does {product_name} offer good value for money?"
            ],
            "comparison": [
                f"How does {product_name} compare to similar products?",
                f"Is {product_name} better than alternatives?",
                f"What makes {product_name} different from competitors?"
            ]
        }

    # ------------------------------------------------------------------
    # LLM-Based Expansion (Optional, Additive Only)
    # ------------------------------------------------------------------

    def _generate_llm_questions(self, product: Dict) -> Dict[str, List[str]]:
        """
        Uses LLM to generate additional question variants.
        Must return STRICT JSON.
        """

        prompt = self._build_llm_prompt(product)
        raw_response = self.llm_client.generate(prompt)

        try:
            parsed = json.loads(raw_response)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        # Fail silently — deterministic baseline remains valid
        return {}

    def _build_llm_prompt(self, product: Dict) -> str:
        return f"""
You are generating user questions for a product content system.

Rules:
- Use ONLY the provided product data
- Do NOT add or infer new facts
- Do NOT answer the questions
- Generate only question variants
- Output STRICTLY valid JSON
- Keys must be exactly: {self.CATEGORIES}

Product Data:
{json.dumps(product, indent=2)}

Output Format:
{{
  "informational": [string],
  "usage": [string],
  "safety": [string],
  "ingredients": [string],
  "pricing": [string],
  "comparison": [string]
}}
        """

    # ------------------------------------------------------------------
    # Merge & Validation
    # ------------------------------------------------------------------

    def _merge_questions(
        self,
        base: Dict[str, List[str]],
        extra: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Merge LLM-generated questions additively.
        """

        for category in self.CATEGORIES:
            if category in extra and isinstance(extra[category], list):
                base[category].extend(extra[category])

        # Deduplicate while preserving order
        for category, questions in base.items():
            seen = set()
            base[category] = [
                q for q in questions
                if not (q in seen or seen.add(q))
            ]

        return base

    def _validate_output(self, questions: Dict[str, List[str]]) -> None:
        """
        Enforces strict schema and minimum guarantees.
        """

        for category in self.CATEGORIES:
            if category not in questions:
                raise ValueError(f"Missing category: {category}")

            if not isinstance(questions[category], list):
                raise ValueError(
                    f"Category '{category}' must be a list"
                )

            if len(questions[category]) < self.MIN_QUESTIONS_PER_CATEGORY:
                raise ValueError(
                    f"Category '{category}' has fewer than "
                    f"{self.MIN_QUESTIONS_PER_CATEGORY} questions"
                )

            for q in questions[category]:
                if not isinstance(q, str) or "?" not in q:
                    raise ValueError(
                        f"Invalid question detected in '{category}': {q}"
                    )

    # ------------------------------------------------------------------
    # Final Shape Conversion (Critical)
    # ------------------------------------------------------------------

    def _flatten_questions(self, questions: Dict[str, List[str]]) -> List[Dict]:
        """
        Converts categorized questions into a flat list of
        {category, question} objects for downstream agents.
        """

        flattened = []

        for category, qs in questions.items():
            for q in qs:
                flattened.append({
                    "category": category,
                    "question": q
                })

        return flattened
