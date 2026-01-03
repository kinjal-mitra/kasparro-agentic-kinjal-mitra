from typing import List, Literal
from pydantic import BaseModel


class FAQItem(BaseModel):
    category: str
    question: str
    answer: str


class FAQPageSchema(BaseModel):
    page_type: Literal["faq"]
    total_questions: int
    questions: List[FAQItem]
