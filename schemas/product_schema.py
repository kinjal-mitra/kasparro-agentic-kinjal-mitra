from typing import Dict, Literal
from pydantic import BaseModel, Field


class ProductPageSchema(BaseModel):
    page_type: Literal["product"]
    content: Dict


#str = Field("product", const=True)