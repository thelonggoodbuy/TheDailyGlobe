from typing import List, Optional
from src.presentation.schemas.base_schemas import BaseSchema
from pydantic import Field





class SubscriptionResponseSchema(BaseSchema):
    # user_id: int
    expiration_date: Optional[str] = Field(default=None, alias='expirationDate')
    is_active: bool = Field(alias='isActive')