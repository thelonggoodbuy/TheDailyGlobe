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
    user_id: int
    article_id: int
    is_sender: bool
    user_email: str



class CommentResponseData(BaseResponseSchema):
    """
    Schema of response for comments.
    """
    data: Optional[List[CommentSchema] | CommentSchema]