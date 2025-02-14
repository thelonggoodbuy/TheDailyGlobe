import hashlib
import os
from src.domain.enums.database import TransactionsStatusEnum
from src.domain.entities.users.users_entities import SubscriptionEntity, TranscationEntity
from src.application.interfaces.repositories import BaseTransactionsRepository, IAlchemyRepository, BaseSubscribtionRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.subscriptions import SubscriptionResponseSchema
from sqlalchemy import select



class TransactionsRepository(BaseTransactionsRepository, IAlchemyRepository):

    async def create_transaction(self, subscription_id):
        order_id = await self.generate_uniq_order_id()
        new_transaction = TranscationEntity(
            order_id=order_id,
            subscription_id=subscription_id,
            status=TransactionsStatusEnum.IN_PROCESS
            )
        self._session.add(new_transaction)
        await self._session.commit()
        return new_transaction
    
    
    async def generate_uniq_order_id(self):
        while True:
            new_transaction_code = hashlib.sha256(os.urandom(32)).hexdigest()
            query_for_search_transaction_with_this_code = \
                select(TranscationEntity).filter(TranscationEntity.order_id == new_transaction_code)
            
            result = await self._session.execute(query_for_search_transaction_with_this_code)
            transaction = result.scalar_one_or_none()
            if not transaction:
                return new_transaction_code


    #TODO: test fuction only for debug:
    async def print_all_transaction(self):
        query = select(TranscationEntity).filter()
        transactions_rows = await self._session.execute(query)
        transactions = transactions_rows.scalars().all()
        for transaction in transactions:
            print('***')
            print(transaction.id)
            print(transaction.status)
            print(transaction.subscription_id)
            print(transaction.order_id)
            print('***')

