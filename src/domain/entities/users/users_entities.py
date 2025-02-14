from dataclasses import dataclass
from src.domain.common.entity import Entity

from advanced_alchemy.types import DateTimeUTC
from enum import Enum
from src.domain.enums.database import SubscriptionType, DeviceType, TransactionsStatusEnum
from typing import Optional

# entity for user object
@dataclass
class UserEntity(Entity):
    """User model."""
    email: str
    password: str
    id: str = None
    is_staff: bool = False
    is_active: bool = True


@dataclass
class SubscriptionEntity(Entity):
    """Subscription model."""
    user_id: int
    expiration_date: Optional[DateTimeUTC] = None
    id: Optional[int] = None
    is_active: bool = False




@dataclass
class UnregisteredDeviceEntity(Entity):
    """Unregistered device model"""
    device_id: str
    device_type: DeviceType
    readed_articles: int
    registration_id: str


@dataclass
class TokenBlacklistEntity(Entity):
    """Blacklist model"""
    access_token: str
    refresh_token: str
    added_date: DateTimeUTC


@dataclass
class TranscationEntity(Entity):
    status: TransactionsStatusEnum
    subscription_id: int
    order_id: str