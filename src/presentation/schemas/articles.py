from pydantic import BaseModel, Field
from typing import List, Optional

from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema

from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake


class ArticlesFeedRequestSchema(BaseSchema):
    category_id: int = Field(alias='categoryId')
    pagination_length: int = Field(alias='paginationLength')
    current_pagination_position: int = Field(alias='currentPaginationPosition')



class ArticleItem(BaseSchema):
    category_title: str = Field(alias='categoryTitle')
    id: int
    title: str
    author: str
    main_image: str = Field(alias='mainImage')
    publication_date: str = Field(alias='publicationDate')


class ArticleFeedResponseSchema(BaseResponseSchema):
    
    data: Optional[List]



class ArticlesDetailRequestSchema(BaseSchema):
    article_id: int = Field(alias='articleId')


class ArticlesDetailResponseSchema(BaseResponseSchema):
    data: dict



class GetSlideshowRequestSchema(BaseSchema):
    article_id: int = Field(alias='articleId')
    article_section_with_slideshow_id: int = Field(alias='articleSectionWithSlideshowId')


class SingleSlideSchema(BaseSchema):
    id: int
    text: str
    image: str
    is_opened: bool = False


class SlideShowResponseSchema(BaseResponseSchema):
    data: List[SingleSlideSchema]




class ArticleSectionPlainTextSchema(BaseModel):
    id: int
    article_id: int = Field(alias='articleId')
    text: str
    intex_number_in_article: int = Field(alias='intexNumberInArticle')
    section_type: str = Field(default="article_sections_with_plain_text", alias='sectionType')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,    
    )



class ArticleSectionSlideShowSchema(BaseModel):
    id: int
    article_id: int = Field(alias='articleId')
    text: str
    intex_number_in_article: int
    image: str
    section_type: str = Field(default="article_section_with_slide_show", alias='sectionType')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
        
        



class ArticleWithVideoSectionSchema(BaseModel):
    id: int
    article_id: int = Field(alias='articleId')
    text: str
    intex_number_in_article: int
    video_url: str
    section_type: str = Field(default="article_section_with_video", alias='sectionType')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ArticleDetailSchema(BaseSchema):
    id: int
    title: str
    main_image: str = Field(alias='mainImage')
    category_id: int
    lead: str
    author: str
    publication_date: str
    category_title: str = Field(alias='categoryTitle')
    article_sections: Optional[List] = Field(alias='articleSections')



    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class GetVideoSchema(BaseSchema):
    """
    Schema of request for video article section.
    Args:
    - id (int) - id of concrete concrete video article section.
    """
    id: int


class VideoArticlSections(BaseSchema):
    """
    Schema of response object for video article section.
    Args:
    - id (int)
    - 
    """
    id: int
    text: str
    video_url: str


class VideoResponseSchema(BaseResponseSchema):
    """
    Schema of response for video article section.
    Args:
    - id (int) - id of concrete concrete video article section.
    """
    data: Optional[VideoArticlSections]