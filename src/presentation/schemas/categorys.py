from pydantic import BaseModel
from typing import List
from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema



class CategoryResponseItem(BaseSchema):
    id: int
    title: str
    extended_title: str


class CategorysResponse(BaseModel):
    categories: List[CategoryResponseItem]
