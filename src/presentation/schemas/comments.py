from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema
from typing import List, Optional
from pydantic import Field





class CreateCommentRequestData(BaseSchema):
    """
    Schema of response object for video article section.
    Args:
    - text (str) - comment`s text
    - article_id (int)
    """
    text: str
    article_id: int = Field(alias='articleId')


class CommentSchema(BaseSchema):
    """
    Schema of comments objects.
    """
    id: int
    text: str
    user_id: int = Field(alias='userId')
    article_id: int = Field(alias='articleId')
    is_sender: bool = Field(alias='isSender')
    user_email: str = Field(alias='userEmail')


class CommentListrIteamSchema(BaseSchema):
    """
    Schema of comments objects for list of comments.
    """
    id: int
    text: str
    # user_id: int
    # article_id: int
    is_sender: bool = Field(alias='isSender')
    user_email: str = Field(alias='userEmail')



class CommentResponseData(BaseResponseSchema):
    """
    Schema of response for comments.
    """
    data: Optional[List[CommentSchema] | CommentSchema | List[CommentListrIteamSchema]]
    # data: dict


class AllCommentRequestData(BaseSchema):
    """
    Schema of request for comments.
    """
    article_id: int = Field(alias='articleId')