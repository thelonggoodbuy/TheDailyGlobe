from abc import ABC, abstractmethod
from src.application.interfaces.repositories import IAlchemyRepository, BaseNotificationsRepository
from src.domain.entities.notifications.notification_entities import NotificationCredentialEntity
from src.domain.entities.articles.articles_entities import CategoryEntity
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload



class NotificationsAlchemyRepository(BaseNotificationsRepository, IAlchemyRepository):
    
    async def save_registration_token(self, token, user_id):

        new_notification_credential = NotificationCredentialEntity(
            registraion_token=token,
            user_id=user_id
        )
        self._session.add(new_notification_credential)
        await self._session.commit()
        await self._session.refresh(new_notification_credential)

        return new_notification_credential
    

    async def get_notification_credential(self, update_notification_data):
        query = select(NotificationCredentialEntity).options(
                                                    selectinload(NotificationCredentialEntity.choosen_categories)
                                                    ).where(NotificationCredentialEntity.registraion_token == update_notification_data.registration_token)
        notification_credential_query_obj = await self._session.execute(query)
        notification_credential = notification_credential_query_obj.scalar()
        return notification_credential



    async def update_notifications_status(self, update_notification_data, category, user_id, notification_credential):
        
        category = await self._session.merge(category)
        if update_notification_data.is_active == True and\
            category not in notification_credential.choosen_categories:
            notification_credential.choosen_categories.append(category)
        elif update_notification_data.is_active == False and\
            category in notification_credential.choosen_categories:
            notification_credential.choosen_categories.remove(category)

        self._session.add(notification_credential)
        await self._session.commit()

        return update_notification_data
    

    async def return_all_notification_objects_per_registration_token(self, registration_token):
        query = select(NotificationCredentialEntity).options(
                                                    selectinload(NotificationCredentialEntity.choosen_categories)
                                                    ).where(NotificationCredentialEntity.registraion_token == registration_token)
        notification_credential_query_obj = await self._session.execute(query)
        notification_credential = notification_credential_query_obj.scalar()

        return notification_credential




    
    async def add_category_to_notification_credential(self, category_id, notification_credential_id):

                
        query = select(CategoryEntity).filter(CategoryEntity.id == category_id)
        category_obj = await self._session.execute(query)
        category = category_obj.scalar()

        query = select(NotificationCredentialEntity).filter(NotificationCredentialEntity.id == notification_credential_id)
        notification_credential_obj = await self._session.execute(query)
        notification_credential = notification_credential_obj.scalar()

        notification_credential.choosen_categories.add(category)
        self._session.add(notification_credential)
        await self._session.commit()

        return True
