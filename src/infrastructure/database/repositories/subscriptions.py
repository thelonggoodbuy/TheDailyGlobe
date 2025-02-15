from src.domain.enums.database import PeriodTypeEnum, TransactionsStatusEnum
from src.domain.entities.users.users_entities import SubscriptionEntity
from src.application.interfaces.repositories import IAlchemyRepository, BaseSubscribtionRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.subscriptions import SubscriptionResponseSchema
from sqlalchemy import select
from enum import Enum
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import joinedload



class SubscriptionRepository(BaseSubscribtionRepository, IAlchemyRepository):

    async def return_user_subscribtion_by_user_id(self, user_id) -> SubscriptionResponseSchema | None:
        query = select(SubscriptionEntity).filter(SubscriptionEntity.user_id == user_id)
        subscription = await self._session.execute(query)
        result = subscription.scalar_one_or_none()
        return result
    

    async def return_subscribtion_by_id(self, id) -> SubscriptionResponseSchema | None:
        query = select(SubscriptionEntity).filter(SubscriptionEntity.id == id)
        subscription = await self._session.execute(query)
        result = subscription.scalar_one_or_none()
        return result
    

    async def create_subscription(self, user_id):
        new_subscription = SubscriptionEntity(
                user_id=user_id,
                is_active=False
            )
        self._session.add(new_subscription)
        await self._session.commit()
        return new_subscription
    
        
    async def update_subscription_by_subscription_id_and_period(self, subscription_id: int, period: PeriodTypeEnum):
        subscription_obj = await self.return_subscribtion_by_id(id=subscription_id)
        subscription_updated_period = await self.get_updated_period(period)
        subscription_obj.expiration_date = subscription_updated_period
        subscription_obj.is_active = True



    async def get_updated_period(self, period: PeriodTypeEnum):
        match period:
            case PeriodTypeEnum.WEEK:
                return await self.handle_week()
            case PeriodTypeEnum.MONTH:
                return await self.handle_month()
            case PeriodTypeEnum.YEAR:
                return await self.handle_year()
            case _:
                raise ValueError(f"Unsupported period type: {period}")


    async def handle_week(self) -> datetime:
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) 
        return tomorrow + timedelta(weeks=1)
        


    async def handle_month(self) -> datetime:
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return tomorrow + relativedelta(months=1)


    async def handle_year(self) -> datetime:
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return tomorrow + relativedelta(years=1)