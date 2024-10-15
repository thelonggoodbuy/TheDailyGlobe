from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import registry
from advanced_alchemy.types import DateTimeUTC
from src.domain.entities.users.users_entities import UserEntity,\
                                                SubscriptionEntity, SubscriptionType,\
                                                UnregisteredDeviceEntity, DeviceType

from src.domain.entities.comments.comments_entities import CommentEntity

# TODO Trouble with mapper registry path here!
from src.infrastructure.database.metadata import mapper_registry



# mapper_registry = registry(metadata=metadata)

# print('=======users tables==============')
# print("Registering UserTable...")
# print(f"Registry ID in {__name__}: {id(mapper_registry)}")

UserTable = Table(
    # Table name
    "users",
    # Metadata
    mapper_registry.metadata,
    #Unique identifier for user
    Column("id", Integer, primary_key=True, autoincrement=True),
    # users email
    Column("email", String(length=255), nullable=False),
    # users password
    Column("password", String(length=255), nullable=False),
    # is_staff field (default False)
    Column("is_staff", Boolean, default=False, nullable=False),
    # is_active field (default False)
    Column("is_active", Boolean, default=False, nullable=False)
    )

# Map the User class to the user_table
# print("Mapping UserTable...")

mapper_registry.map_imperatively(
    UserEntity,
    UserTable,
    properties={
        "subscription": relationship(SubscriptionEntity, back_populates="user"),
        "comments": relationship(CommentEntity, back_populates="user")

    }    
)

SubscriptionTable = Table(
    # Table name
    "subscriptions",
    # Metadata
    mapper_registry.metadata,
    # Unique identifier for subscription
    Column("id", Integer, primary_key=True, autoincrement=True),
    # One to one relationship with users
    Column("user_id", ForeignKey("users.id"), unique=True),
    # expiration date of subscription
    Column("expiration_date",
        DateTimeUTC(timezone=True),
        nullable=False,
    ),
    Column("subscription_type",
        SQLAlchemyEnum(SubscriptionType, name="subscription_type"), 
        nullable=False),
)

# Map the Subscription class to the subscriptions_table
mapper_registry.map_imperatively(
    SubscriptionEntity,
    SubscriptionTable,
    properties={
        "user": relationship(UserEntity, back_populates="subscription"),
        "comments": relationship(CommentEntity, back_populates="article")
    }
)


UnregisteredDeviceTable = Table(
    # Table name
    "unregistered_devices",
    # Metadata
    mapper_registry.metadata,
    # Unique identifier for unregistered device
    Column("id", Integer, primary_key=True, autoincrement=True),
    # unique device identifier
    Column("device_id", String(length=255), nullable=False),
    # device type - ios or android os
    Column("device_type", SQLAlchemyEnum(DeviceType, name="device_type"), nullable=False),
    # readed articles today for unregistered device
    Column("readed_articles", Integer),
)

mapper_registry.map_imperatively(
    UnregisteredDeviceEntity,
    UnregisteredDeviceTable
)






# print("Registered tables in Users module:")
# print(mapper_registry.metadata.tables.keys())