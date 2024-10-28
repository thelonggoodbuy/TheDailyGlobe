from pydantic import BaseModel
from typing import List

from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema




class ArticlesFeedRequestSchema(BaseModel):
    category_id: int = None
    pagination_length: int
    current_pagination_position: int



class ArticleItem(BaseResponseSchema):
    category_title: str
    id: int
    title: str
    author: str
    main_image: str
    publication_date: str


class ArticleFeedResponseSchema(BaseResponseSchema):
    articles: List[ArticleItem]



class ArticlesDetailRequestSchema(BaseModel):
    article_id: int


class ArticlesDetailResponseSchema(BaseModel):
    response_dict: dict



class GetSlideshowRequestSchema(BaseModel):
    article_id: int
    article_section_with_slideshow_id: int


class SingleSlideSchema(BaseModel):
    id: int
    text: str
    image: str
    is_opened: bool = False


class SlideShowResponseSchema(BaseModel):
    result: List[SingleSlideSchema]