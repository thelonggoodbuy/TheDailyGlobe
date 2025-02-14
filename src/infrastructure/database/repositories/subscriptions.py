from src.domain.entities.users.users_entities import SubscriptionEntity
from src.application.interfaces.repositories import IAlchemyRepository, BaseSubscribtionRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.subscriptions import SubscriptionResponseSchema
from sqlalchemy import select



class SubscriptionRepository(BaseSubscribtionRepository, IAlchemyRepository):
    async def return_user_subscribtion_by_user_id(self, user_id) -> SubscriptionResponseSchema | None:

        query = select(SubscriptionEntity).filter(SubscriptionEntity.user_id == user_id)
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
    
        