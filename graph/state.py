from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    # ------------------
    # Input
    # ------------------
    raw_product_a: Dict
    raw_product_b: Dict

    # ------------------
    # Parsed
    # ------------------
    normalized_product_a: Optional[Dict] = None
    normalized_product_b: Optional[Dict] = None
    parse_errors: List[str] = Field(default_factory=list)

    # ------------------
    # Questions
    # ------------------
    generated_questions: List[Dict] = Field(default_factory=list)
    question_count: int = 0
    question_generation_attempts: int = 0
    max_question_generation_attempts: int = 5
    min_required_questions: int = 15


    # ------------------
    # FAQ Context & Answers
    # ------------------
    faq_context_map: Dict = Field(default_factory=dict)
    faq_answers: List[Dict] = Field(default_factory=list)
    faq_answer_errors: List[str] = Field(default_factory=list)

    # ------------------
    # Pages
    # ------------------
    faq_page: Optional[Dict] = None
    product_page: Optional[Dict] = None
    comparison_page: Optional[Dict] = None

    # ------------------
    # Validation & Control
    # ------------------
    schema_validation_errors: Dict = Field(default_factory=dict)
    retry_flags: Dict = Field(default_factory=dict)
    execution_log: List[str] = Field(default_factory=list)
