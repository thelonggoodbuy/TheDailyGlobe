from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import registry
from advanced_alchemy.types import DateTimeUTC
from src.domain.entities.articles.articles_entities import ArticleEntity
from sqlalchemy_file import FileField

from src.domain.entities.articles.articles_entities import ArticleWithPlainTextSectionEntity,\
                                ArticleSectionSlideShowEntity,\
                                ArticleWithVideoSectionEntity,\
                                CategoryEntity, ArticleSectionEntity

from src.domain.entities.comments.comments_entities import CommentEntity

from src.infrastructure.database.metadata import mapper_registry
from src.infrastructure.database.utilities.save_file_field import SaveFileField


# category table
CategortyTable = Table(
    "category",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(length=255), nullable=False)

)

# mapper categories
# print("Mapping CategortyTable...")
mapper_registry.map_imperatively(
    CategoryEntity,
    CategortyTable,
    properties={
        "article": relationship(ArticleEntity, back_populates="article"),
    }
)

# print("Registering ArticleTable...")
ArticleTable = Table(
    # Table name
    "articles",
    # Metadata
    mapper_registry.metadata,
    # Unique identifier for article
    Column("id", Integer, primary_key=True, autoincrement=True),
    # article`s title
    Column("title", String(length=255), nullable=False),
    # article`s category FK
    Column("category_id", ForeignKey("category.id")),
    # article's lead
    Column("lead", Text),
    # article's author
    Column("author", String(length=255), nullable=False),
    # publication date
    Column("publication_date", 
        DateTimeUTC(timezone=True),
        nullable=False,
        )
)

# Map the Category class to the category_table
# print("Mapping ArticleTable...")

mapper_registry.map_imperatively(
    ArticleEntity,
    ArticleTable,
    properties={
        "category": relationship(CategoryEntity, back_populates="article"),
        "comments": relationship(CommentEntity, back_populates="article")
    }
)




# article section with plain text
ArticleSectionPlainTextTable = Table(
    "article_sections_with_plain_text",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("article_id", ForeignKey("articles.id")),
    Column("text", Text, nullable=False),
    Column("intex_number_in_article", Integer, nullable=False),
)

# mapping article section with plain text
mapper_registry.map_imperatively(
    ArticleWithPlainTextSectionEntity,
    ArticleSectionPlainTextTable,
    properties={
        "article": relationship(ArticleEntity, back_populates="article_section_with_plain_text")
    }
)


# article section with image
ArticleSectionSlideShowTable = Table(
    "article_section_with_slide_show",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("article_id", ForeignKey("articles.id")),
    Column("text", Text, nullable=False),
    Column("intex_number_in_article", Integer, nullable=False),
    Column("image", SaveFileField(length=255), nullable=False)
)


# mapping article section with image
mapper_registry.map_imperatively(
    ArticleSectionSlideShowEntity,
    ArticleSectionSlideShowTable,
    properties={
        "article": relationship(ArticleEntity, back_populates="article_section_with_slide_show")
    }
)



# article section with video
ArticleSectionVideoTable = Table(
    "article_section_with_video",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("article_id", ForeignKey("articles.id")),
    Column("text", Text, nullable=False),
    Column("intex_number_in_article", Integer, nullable=False),
    Column("video_url", String(length=255), nullable=False)
)


# Mapping article section with videl
mapper_registry.map_imperatively(
    ArticleWithVideoSectionEntity,
    ArticleSectionVideoTable,
        properties={
        "article": relationship(ArticleEntity, back_populates="article_section_with_video")
    }
)



# print("Registered tables in Articles module:")
# print(mapper_registry.metadata.tables.keys())