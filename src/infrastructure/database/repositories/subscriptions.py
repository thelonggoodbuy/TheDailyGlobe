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
        print('---user_id---in---subscription---')
        print(user_id)
        print('---------------------------------')
        print(result)
        print('---------------------------------')
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
        if not subscription_obj.expiration_date or subscription_obj.expiration_date < datetime.now(timezone.utc):
            subscription_updated_period = await self.new_updated_period(period)
        else:
            subscription_updated_period = await self.add_to_updated_period(period, finish_date=subscription_obj.expiration_date)

        subscription_obj.expiration_date = subscription_updated_period
        subscription_obj.is_active = True
        self._session.add(subscription_obj)
        await self._session.commit()
        return subscription_obj


    async def add_to_updated_period(self, period: PeriodTypeEnum, finish_date):
        match period:
            case PeriodTypeEnum.WEEK:
                return await self.handle_week(finish_date)
            case PeriodTypeEnum.MONTH:
                return await self.handle_month(finish_date)
            case PeriodTypeEnum.YEAR:
                return await self.handle_year(finish_date)
            case _:
                raise ValueError(f"Unsupported period type: {period}")


    async def new_updated_period(self, period: PeriodTypeEnum):
        match period:
            case PeriodTypeEnum.WEEK:
                return await self.handle_week()
            case PeriodTypeEnum.MONTH:
                return await self.handle_month()
            case PeriodTypeEnum.YEAR:
                return await self.handle_year()
            case _:
                raise ValueError(f"Unsupported period type: {period}")


    async def handle_week(self, finish_date=None) -> datetime:
        if finish_date:
            result = finish_date + timedelta(weeks=1)
        else:
            now = datetime.now(timezone.utc)
            tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) 
            result = tomorrow + timedelta(weeks=1)
        return result
        

    async def handle_month(self, finish_date=None) -> datetime:
        if finish_date:
            result = finish_date + relativedelta(months=1)
        else:
            now = datetime.now(timezone.utc)
            tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            result = tomorrow + relativedelta(months=1)
        return result


    async def handle_year(self, finish_date=None) -> datetime:
        if finish_date:
            result = finish_date + relativedelta(years=1)
        else:
            now = datetime.now(timezone.utc)
            tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            result = tomorrow + relativedelta(years=1)
        return result