from sqlalchemy import Numeric, Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import registry
from advanced_alchemy.types import DateTimeUTC
from src.domain.entities.tariffs.tariffs_entities import TariffEntity
from src.domain.enums.database import CurencyType, PeriodTypeEnum, TransactionsStatusEnum
from src.domain.entities.users.users_entities import TokenBlacklistEntity, TranscationEntity, UserEntity,\
                                                SubscriptionEntity, SubscriptionType,\
                                                UnregisteredDeviceEntity, DeviceType

from src.domain.entities.comments.comments_entities import CommentEntity

# TODO Trouble with mapper registry path here!
from src.infrastructure.database.metadata import mapper_registry
from src.domain.entities.notifications.notification_entities import NotificationCredentialEntity


UserTable = Table(
    # Table name
    "users",
    # Metadata
    mapper_registry.metadata,
    #Unique identifier for user
    Column("id", Integer, primary_key=True, autoincrement=True),
    # users email
    Column("email", String(length=255), nullable=False, unique=True),
    # users password
    Column("password", String(length=255), nullable=False),
    # is_staff field (default False)
    Column("is_staff", Boolean, default=False, nullable=False),
    # is_active field (default False)
    Column("is_active", Boolean, default=False, nullable=False)
    )


mapper_registry.map_imperatively(
    UserEntity,
    UserTable,
    properties={
        "subscription": relationship(SubscriptionEntity, back_populates="user"),
        "comments": relationship(CommentEntity, back_populates="user"),
        "user_notification": relationship(NotificationCredentialEntity, back_populates="user")

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
        nullable=True,
    ),
    Column("is_active", Boolean),
)

# Map the Subscription class to the subscriptions_table
mapper_registry.map_imperatively(
    SubscriptionEntity,
    SubscriptionTable,
    properties={
        "user": relationship(UserEntity, back_populates="subscription"),
        "transactions": relationship(TranscationEntity, back_populates="subscription"),
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
    Column("registration_id", String(length=255), nullable=False),
)

mapper_registry.map_imperatively(
    UnregisteredDeviceEntity,
    UnregisteredDeviceTable
)



TokenBlacklistTable = Table(
    "black_list",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("access_token", String(length=1000), nullable=False),
    Column("refresh_token", String(length=1000), nullable=False),
    Column("added_date", DateTimeUTC(timezone=True), nullable=False,)
)

mapper_registry.map_imperatively(
    TokenBlacklistEntity,
    TokenBlacklistTable
)


TariffsTable = Table(
    "tariff",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(length=255), nullable=False),
    Column("subscription_period", SQLAlchemyEnum(PeriodTypeEnum, name="subscription_period")),
    Column("cost", Numeric(10, 2), nullable=False),
    Column("cost_per_year", Numeric(10, 2), nullable=True),
    Column("curency", SQLAlchemyEnum(CurencyType, name="curency_type"), nullable=False),

)

mapper_registry.map_imperatively(
    TariffEntity,
    TariffsTable
)



TranscationsTable = Table(
    "transactions",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status", SQLAlchemyEnum(TransactionsStatusEnum, name="transaction_status")),
    Column("subscription_id", ForeignKey("subscriptions.id")),
    Column("order_id", String(length=255), nullable=False),
)


mapper_registry.map_imperatively(
    TranscationEntity,
    TranscationsTable,
    properties={
        "subscription": relationship(SubscriptionEntity, back_populates="transactions")
    }
)