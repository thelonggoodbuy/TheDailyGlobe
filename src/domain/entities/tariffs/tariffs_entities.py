




from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from src.domain.common.entity import Entity
from src.domain.enums.database import CurencyType, PeriodTypeEnum


@dataclass
class TariffEntity(Entity):
    """Subscription model."""
    id: int
    title: str
    cost: Decimal
    subscription_period: PeriodTypeEnum
    curency: CurencyType
    cost_per_year: Optional[Decimal] = None
