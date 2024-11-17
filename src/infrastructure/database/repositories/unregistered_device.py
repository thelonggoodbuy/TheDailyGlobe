# from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UnregisteredDeviceTable
# from src.infrastructure.database.tables.articles import CategortyTable
from src.domain.entities.users.users_entities import UnregisteredDeviceEntity

from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.subscriptions import SubscriptionResponseSchema
from src.presentation.schemas.articles import ArticlesDetailRequestSchema
from src.domain.enums.database import DeviceType
from sqlalchemy import select, update


# # TODO -> application interfaces
class BaseUnregisteredDeviceRepository(ABC):
    @abstractmethod
    async def get_or_create_unregistered_device():
        raise NotImplementedError
    


class UnregisteredDeviceRepository(BaseUnregisteredDeviceRepository, IAlchemyRepository):
    async def get_or_create_unregistered_device(self, unregistered_device_schema: ArticlesDetailRequestSchema):

        query = select(UnregisteredDeviceEntity).filter(UnregisteredDeviceEntity.registration_id == unregistered_device_schema.unregistered_device.registration_id)
        unregistered_device_obj = await self._session.execute(query)
        result = unregistered_device_obj.scalars().first()

        if result == None:
            print('---ENUM---OBJD----')

            print(unregistered_device_schema.unregistered_device.device_type)
            print('------------------')

            new_unregistered_device = UnregisteredDeviceEntity(
            device_id=unregistered_device_schema.unregistered_device.device_id,
            device_type=DeviceType(unregistered_device_schema.unregistered_device.device_type),
            readed_articles=0,
            registration_id=unregistered_device_schema.unregistered_device.registration_id

            )
            self._session.add(new_unregistered_device)
            await self._session.commit()
            result = new_unregistered_device

        return result
    
    async def add_one_view(self, unregistrated_device: UnregisteredDeviceEntity):
        query = (
        update(UnregisteredDeviceEntity)
        .where(UnregisteredDeviceEntity.registration_id == unregistrated_device.registration_id)
        .values(readed_articles=UnregisteredDeviceEntity.readed_articles + 1)
        )
        await self._session.execute(query)
        
        await self._session.commit()
        return True