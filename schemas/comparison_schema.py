from typing import Dict, Literal
from pydantic import BaseModel, Field


class ComparisonPageSchema(BaseModel):
    page_type: Literal["comparison"]
    comparison: Dict
