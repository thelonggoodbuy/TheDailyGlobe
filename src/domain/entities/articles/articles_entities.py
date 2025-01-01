from dataclasses import dataclass
from src.domain.common.entity import Entity

from advanced_alchemy.types import DateTimeUTC
from enum import Enum
from sqlalchemy_file import FileField
from sqlalchemy.inspection import inspect
from typing import Any

# entity for article object
@dataclass
class ArticleEntity(Entity):
    """Article model."""
    id: int
    title: str
    main_image: str
    category_id: int
    lead: str
    author: str
    publication_date: DateTimeUTC
    viewing: str
    is_premium: bool


@dataclass
class ArticleSectionEntity(Entity):

    """Article section base model. 
    It content all fiels, which are 
    belonged to any article sections"""

    article_id: int
    text: str
    index_number_in_article: int
    section_type: str


@dataclass
class ArticleWithPlainTextSectionEntity(Entity):
    """Model of article section, which content only text content"""
    id: int
    article_id: int
    text: str
    index_number_in_article: int
    section_type: str



@dataclass
class ArticleSectionSlideShowEntity(Entity):
    """Model of article section, which content text and image"""
    
    article_id: int
    text: str
    index_number_in_article: int
    image: str
    section_type: str
    author: str
    # title: str
    id: int = None


@dataclass
class ArticleWithVideoSectionEntity(Entity):
    """Model of article section, which content text and video"""
    id: int
    article_id: int
    title: str
    text: str
    index_number_in_article: int
    video_url: str
    section_type: str
    image_preview: str




@dataclass
class CategoryEntity(Entity):
    id: int
    title: str
    extended_title: str