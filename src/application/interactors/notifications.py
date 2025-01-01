from src.infrastructure.interfaces.uow import IDatabaseSession
from src.application.interfaces.services import INotificationService
from src.main.config.settings import Settings
from src.application.interfaces.repositories import BaseCategoryRepository


from src.presentation.schemas.notifications import SaveOrUpdateNotificationCredesRequestSchema,\
                                                SaveOrUpdateNotificationCredesResponseSchema,\
                                                NotificationCategoryStateObjectSchema,\
                                                ReturnNotificationsStateResponseSchema,\
                                                UpdateNotificationStateRequestSchema,\
                                                NotificationStatusItem,\
                                                ReturnNotificationStatusResponseSchema

from src.application.tasks.notification_tasks import send_notification
from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.application.interfaces.repositories import BaseNotificationsRepository


from fastapi.responses import JSONResponse



class TestNotificationThrowTokenInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        notification_service: INotificationService,
        settings: Settings):

        self.db_session = db_session
        self.notification_service = notification_service
        self.settings = settings


    async def __call__(self, registration_token: str, message: str):
        await self.notification_service.notificate_throw_token(registration_token, message)




class ReturnNotificationCredentialsInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        notification_service: INotificationService,
        settings: Settings):

        self.db_session = db_session
        self.notification_service = notification_service
        self.settings = settings


    async def __call__(self, jwt_token: str, registration_token_data: SaveOrUpdateNotificationCredesRequestSchema):
        
        result = await self.notification_service.save_registration_token(jwt_token, registration_token_data)
        return result


class UpdateNotificationCredentialsInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        notification_service: INotificationService,
        settings: Settings):

        self.db_session = db_session
        self.notification_service = notification_service
        self.settings = settings


    async def __call__(self, jwt_token: str, registration_token_data: SaveOrUpdateNotificationCredesRequestSchema):
        print('===>updating_registration_token_data<===')
        print(jwt_token)
        print(registration_token_data)
        print('===============================')



class GetNotificationsStatusInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        notification_service: INotificationService,
        category_repository: BaseCategoryRepository, 
        settings: Settings):

        self.db_session = db_session
        self.notification_service = notification_service
        self.category_repository = category_repository
        self.settings = settings

    async def __call__(self, registration_token_data):
        total_categories = await self.category_repository.get_all()
        notification_statuses = await self.notification_service.get_notifications_status(registration_token_data.registration_token)

        if not notification_statuses:
            result = BaseResponseSchema(error=True, message="token isnt saved in DB", data={})
            result = JSONResponse(status_code=400, content=result.model_dump())
        else:

            notification_statuses_dict = {}
            
            for category in notification_statuses.choosen_categories:
                notification_statuses_dict[category.id] = category


            notification_status_item_list = []
            for category in total_categories.categories:
                if category.id in notification_statuses_dict.keys():
                    notification_status_item = NotificationStatusItem(
                        category_id=category.id,
                        category_title=category.title,
                        is_active=True
                    )
                    notification_status_item_list.append(notification_status_item)
                else:
                    notification_status_item = NotificationStatusItem(
                        category_id=category.id,
                        category_title=category.title,
                        is_active=False
                    )
                    notification_status_item_list.append(notification_status_item)

            result = ReturnNotificationStatusResponseSchema(
                error=False,
                message="",
                data=notification_status_item_list
            )


        # NotificationStatusItem,\
        # ReturnNotificationStatusResponseSchema

        # send_notification.delay(text="===>Send data from notification!<===")

        return result


class UpdateNotificationsStatusInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        notification_service: INotificationService,
        category_repository: BaseCategoryRepository, 
        notifications_repository: BaseNotificationsRepository,
        settings: Settings):

        self.db_session = db_session
        self.notification_service = notification_service
        self.category_repository = category_repository
        self.notifications_repository = notifications_repository
        self.settings = settings

    async def __call__(self, jwt_token: str, update_notification_data: UpdateNotificationStateRequestSchema):

        from src.presentation.schemas.notifications import ChangedCategoryStatusResponseSchema

        category = await self.category_repository.get_one_by_id(update_notification_data.category_id)

        get_notification_credential = await self.notifications_repository.get_notification_credential(update_notification_data)

        print('===get_notification_credential===')
        print(get_notification_credential)
        print('=================================')
        if get_notification_credential != None:
            print('1')
            result = await self.notification_service.update_notifications_status(jwt_token.credentials, update_notification_data, category, get_notification_credential)
            return ChangedCategoryStatusResponseSchema(error=False, message="", data=result.model_dump(by_alias=True))
            
            
        else:
            print('2')
            return BaseResponseSchema(error=True, message="Registration token is`nt saved in system.", data={})
