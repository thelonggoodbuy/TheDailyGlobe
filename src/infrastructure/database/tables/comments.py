from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import registry
from src.domain.entities.articles.articles_entities import ArticleEntity

from src.domain.entities.comments.comments_entities import CommentEntity
from src.domain.entities.users.users_entities import UserEntity
from src.domain.entities.articles.articles_entities import ArticleEntity

# from src.infrastructure.database.tables.users import UserTable
# from src.infrastructure.database.tables.articles import ArticleTable


from src.infrastructure.database.metadata import mapper_registry


# mapper_registry = registry(metadata=metadata)

# print('=======comment tables==============')
# print(f"Registry ID in {__name__}: {id(mapper_registry)}")

CommentTable = Table(
    # table name
    "comments",
    # Metadata
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", Text),
    Column("user_id", ForeignKey("users.id")),
    Column("article_id", ForeignKey("articles.id")),
)

mapper_registry.map_imperatively(
    CommentEntity,
    CommentTable,
    properties={
        "user": relationship(UserEntity, back_populates="comments"),
        "article": relationship(ArticleEntity, back_populates="comments")
    }
)




# print("Registered tables in Comments module:")
# print(mapper_registry.metadata.tables.keys())