from dataclasses import dataclass
from src.domain.common.entity import Entity

from advanced_alchemy.types import DateTimeUTC
from enum import Enum
from sqlalchemy_file import FileField



# entity for article object
@dataclass
class ArticleEntity(Entity):
    """Article model."""
    title: str
    category_id: int
    lead: str
    author: str
    publication_date: DateTimeUTC



@dataclass
class ArticleSectionEntity(Entity):

    """Article section base model. 
    It content all fiels, which are 
    belonged to any article sections"""

    article_id: int
    text: str
    intex_number_in_article: int
    section_type: str


@dataclass
class ArticleWithPlainTextSectionEntity(Entity):
    """Model of article section, which content only text content"""
    article_id: int
    text: str
    intex_number_in_article: int



@dataclass
class ArticleSectionSlideShowEntity(Entity):
    """Model of article section, which content text and image"""
    article_id: int
    text: str
    intex_number_in_article: int
    image: str


@dataclass
class ArticleWithVideoSectionEntity(Entity):
    """Model of article section, which content text and video"""
    article_id: int
    text: str
    intex_number_in_article: int
    video_url: str



@dataclass
class CategoryEntity(Entity):
    title: str