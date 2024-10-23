from pydantic import BaseModel
from typing import List


class CategoryResponseItem(BaseModel):
    id: int
    title: str


class CategorysResponse(BaseModel):
    categories: List[CategoryResponseItem]
