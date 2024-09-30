from dataclasses import dataclass
from src.domain.common.entity import Entity

from advanced_alchemy.types import DateTimeUTC
from enum import Enum
from src.domain.enums.database import SubscriptionType, DeviceType

# entity for user object
@dataclass
class UserEntity(Entity):
    """User model."""
    email: str
    password: str
    is_staff: bool = False
    is_active: bool = False


@dataclass
class SubscriptionEntity(Entity):
    """Subscription model."""
    user_id: int
    expiration_date: DateTimeUTC
    subscription_type: SubscriptionType




@dataclass
class UnregisteredDeviceEntity(Entity):
    """Unregistered device model"""
    device_id: str
    device_type: DeviceType
    readed_articles: int