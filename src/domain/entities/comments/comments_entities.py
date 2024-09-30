from dataclasses import dataclass
from src.domain.common.entity import Entity

from advanced_alchemy.types import DateTimeUTC
from enum import Enum
from sqlalchemy_file import FileField



# entity for comment object
@dataclass
class CommentEntity(Entity):
    """Comment model."""
    text: str
    user_id: int
    article_id: int
