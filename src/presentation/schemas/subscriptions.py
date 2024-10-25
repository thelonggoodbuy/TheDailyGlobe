from pydantic import BaseModel
from typing import List



class SubscriptionResponseSchema(BaseModel):
    user_id: int
    expiration_date: str = None
    subscription_type: str = None