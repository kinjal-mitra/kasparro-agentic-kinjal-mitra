from typing import Dict


class AnswerGenerationAgent:
    """
    Generates a specific FAQ answer for a single question
    using structured product data, category context,
    and a controlled prompt.

    This agent is the ONLY place where the LLM is invoked
    for FAQ answer generation.
    """

    def __init__(self, llm_client):
        """
        Parameters
        ----------
        llm_client : object
            Predefined LLM client already available in the system.
            Must expose a `generate(prompt: str) -> str` method.
        """
        self.llm = llm_client

    def generate_answer(self, product: Dict, category: str, question: str, supporting_context: Dict, 
                        prompt_template: str = "faq_answer_v1",) -> Dict:
        """
        Generate an answer for a single FAQ question.

        Parameters
        ----------
        product : Dict
            Normalized product data
        category : str
            Category of the question (Safety, Usage, Purchase, etc.)
        question : str
            The exact question text
        supporting_context : Dict
            Output from relevant content logic blocks
        prompt_template : str
            Prompt template identifier

        Returns
        -------
        Dict
            {
                "question": <question>,
                "answer": <generated_answer>
            }
        """
        prompt = self._build_prompt(product=product, category=category, question=question,
                                    supporting_context=supporting_context,prompt_template=prompt_template,)

        answer_text = self.llm.generate(prompt)

        return {
            "question": question,
            "answer": self._postprocess_answer(answer_text),
        }

    # -------------------------
    # Internal Helpers
    # -------------------------

    def _build_prompt(self, product: Dict, category: str, question: str, supporting_context: Dict, prompt_template: str,) -> str:
        """
        Builds a deterministic prompt for the LLM.
        """

        if prompt_template != "faq_answer_v1":
            raise ValueError(f"Unknown prompt template: {prompt_template}")

        return f"""
                You are generating an FAQ answer for a skincare product.

                Product data:
                {product}

                Additional context:
                {supporting_context}

                Category:
                {category}

                Question:
                {question}

                Rules:
                - Use ONLY the provided product data
                - Do NOT add external facts
                - Answer in 1 to 2 clear sentences
                - Be specific to the question
                - Do NOT mention the category explicitly
                """.strip()

    def _postprocess_answer(self, answer: str) -> str:
        """
        Cleans and normalizes LLM output.
        """
        if not answer:
            return ""

        # Remove accidental leading/trailing whitespace or quotes
        answer = answer.strip().strip('"').strip("'")

        return answer
