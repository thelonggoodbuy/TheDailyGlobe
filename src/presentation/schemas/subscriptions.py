from decimal import Decimal
from typing import List, Optional
from src.presentation.schemas.base_schemas import BaseSchema
from pydantic import Field





class SubscriptionResponseSchema(BaseSchema):
    # user_id: int
    expiration_date: Optional[str] = Field(default=None, alias='expirationDate')
    is_active: bool = Field(alias='isActive')


class TariffRequestSchema(BaseSchema):
    tariff_id: int = Field(default=None, alias="tariffId")


class TariffItemSchema(BaseSchema):
    id: int
    title: str
    cost: Decimal
    cost_per_year: Optional[Decimal] = Field(default=None, alias="costPerYear")


class AllTariffResponseSchema(BaseSchema):
    tariff_list: List[TariffItemSchema]