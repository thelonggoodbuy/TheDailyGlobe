from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey, Text, Boolean
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
from sqlalchemy import Index, text




# category table
CategortyTable = Table(
    "category",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(length=255), nullable=False),
    Column("extended_title", String(length=255), nullable=False),

)

# mapper categories
# print("Mapping CategortyTable...")
mapper_registry.map_imperatively(
    CategoryEntity,
    CategortyTable,
    properties={
        "article": relationship(ArticleEntity, back_populates="category"),
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
    Column("main_image", String(length=255), nullable=False),
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
        ),
    Column("viewing", Integer, default=0),
    Column("is_premium", Boolean, default=False),

    Index('title_index', "title", postgresql_using="gin", postgresql_ops={"title": "gin_trgm_ops"}),
    

    # __table_args__ = (
         
    # )

    # __table_args__ = (
    #     Index("article_title_idx", "title", postgresql_using="gin", postgresql_ops={"title": "gin_trgm_ops"}),
    #     Index("article_lead_idx", "lead", postgresql_using="gin", postgresql_ops={"lead": "gin_trgm_ops"}),
    # )
    
)

    
# Map the Category class to the category_table
# print("Mapping ArticleTable...")

mapper_registry.map_imperatively(
    ArticleEntity,
    ArticleTable,
    properties={
        "category": relationship(CategoryEntity, back_populates="article"),
        "comments": relationship(CommentEntity, back_populates="article"),
        "article_section_with_plain_text": relationship(ArticleWithPlainTextSectionEntity, back_populates="article"),
        "article_section_with_slide_show": relationship(ArticleSectionSlideShowEntity, back_populates="article"),
        "article_section_with_video": relationship(ArticleWithVideoSectionEntity, back_populates="article"),
    }
)




# article section with plain text
ArticleSectionPlainTextTable = Table(
    "article_sections_with_plain_text",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("article_id", ForeignKey("articles.id")),
    Column("text", Text, nullable=False),
    Column("index_number_in_article", Integer, nullable=False),
    Column("section_type", String(length=50), default="article_sections_with_plain_text", nullable=False)
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
    Column("index_number_in_article", Integer, nullable=False),
    Column("image", String(length=255), nullable=False),
    Column("author", String(length=255), nullable=False),
    Column("section_type", String(length=50), default="article_section_with_slide_show", nullable=False)
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
    Column("title", String(length=255), nullable=False),
    Column("text", Text, nullable=False),
    Column("index_number_in_article", Integer, nullable=False),
    Column("video_url", String(length=255), nullable=False),
    Column("section_type", String(length=50), default="article_section_with_video", nullable=False),
    Column("image_preview", String(length=255), nullable=False),
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