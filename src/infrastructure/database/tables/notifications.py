from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.infrastructure.database.metadata import mapper_registry
from src.domain.entities.notifications.notification_entities import NotificationCredentialEntity
from src.domain.entities.users.users_entities import UserEntity
from src.domain.entities.articles.articles_entities import CategoryEntity
from sqlalchemy.orm import relationship





NotificationCredentialTable = Table(
    # table name
    "notification_credential",
    # Metadata
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("registraion_token", String(length=255), nullable=False),
    Column("user_id", ForeignKey("users.id")),

)


# NotificationCredentialCategory
CategoryNotificationCredetialTable = Table(
    'category_notification_credetial', 
    mapper_registry.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('notification_credential_id', Integer, ForeignKey('notification_credential.id'), primary_key=True)
)




mapper_registry.map_imperatively(
    NotificationCredentialEntity,
    NotificationCredentialTable,
    properties={
        "user": relationship(UserEntity, back_populates="user_notification"),
        "choosen_categories": relationship(CategoryEntity, secondary=CategoryNotificationCredetialTable, back_populates="notification_credential")
    }
)

