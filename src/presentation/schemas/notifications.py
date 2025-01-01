from typing import List, Optional
from src.presentation.schemas.base_schemas import BaseSchema, BaseResponseSchema
from pydantic import Field





class SaveOrUpdateNotificationCredesRequestSchema(BaseSchema):
    registration_token: str = Field(alias='registrationToken')


class SaveOrUpdateNotificationCredesResponseSchema(BaseResponseSchema):
    data: dict



class NotificationCategoryStateObjectSchema(BaseSchema):
    category_title: str = Field(alias='categoryTitle')
    category_id: int = Field(alias='categoryId')
    is_active: bool = Field(alias='isActive')


class ReturnNotificationsStateResponseSchema(BaseResponseSchema):
    data: List[NotificationCategoryStateObjectSchema]


class UpdateNotificationStateRequestSchema(BaseSchema):
    category_id: int = Field(alias='categoryId')
    is_active: bool = Field(alias='isActive')
    registration_token: str = Field(alias='registrationToken')


class NotificationStatusItem(BaseSchema):
    category_id: int = Field(alias='categoryId')
    category_title: str = Field(alias='categoryTitle')
    is_active: bool = Field(alias='isActive')


class ReturnNotificationStatusResponseSchema(BaseResponseSchema):
    data: List[NotificationStatusItem]


    
class ChangedCategoryStatus(BaseSchema):
    category_id: int = Field(alias='categoryId')
    is_active: bool = Field(alias='isActive')

class ChangedCategoryStatusResponseSchema(BaseResponseSchema):
    data: ChangedCategoryStatus