import firebase_admin.app_check
from src.application.interfaces.services import INotificationService
from src.application.interfaces.repositories import BaseNotificationsRepository
from src.application.interfaces.services import ITokenService


from src.main.config.settings import Settings
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin._messaging_utils import UnregisteredError
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.presentation.schemas.base_schemas import BaseResponseSchema
 




class NotificationFirebaseService(INotificationService):
    """ Service for notification throw firebase """

    def __init__(
        self,
        settings: Settings,
        token_service: ITokenService,
        notifications_repository: BaseNotificationsRepository
    ):
        # """Initialize Jwt token settings."""
        self.settings = settings
        self.notifications_repository = notifications_repository
        self.token_service = token_service



    async def save_registration_token(self, jwt_token, registration_token):
        user = await self.token_service.get_user_by_token(jwt_token)
        user_notification_obj = await self.notifications_repository.get_or_activate_notification_obj(registration_token, user.id)     
        try:
            firebase_app = firebase_admin.get_app(name="firebase_app")

            message = messaging.Message(
            notification=messaging.Notification(
                title=f"TDG: привіт!",
                body=f"Ви зайшли в додаток The daily globe!\nОберіть категорії для сповіщень"
            ),
            token=registration_token,)

            response = messaging.send(message, app=firebase_app)
            if not user_notification_obj:
                await self.notifications_repository.save_registration_token(registration_token, user_id=user.id)
            result = BaseResponseSchema(error=False, message="", data={})
            result = JSONResponse(status_code=200, content=result.model_dump())
        except UnregisteredError:
            result = BaseResponseSchema(error=True, message="Invalid registration token provided", data={})
            result = JSONResponse(status_code=400, content=result.model_dump())
        except ValueError:
            result = BaseResponseSchema(error=True, message="Invalid registration token provided", data={})
            result = JSONResponse(status_code=400, content=result.model_dump())
        except Exception as e:

            result = BaseResponseSchema(error=True, message="Invalid registration token provided", data={})
            result = JSONResponse(status_code=400, content=result.model_dump())

        return result
    

    async def update_notifications_status(self, jwt_token, update_notification_data, category, get_notification_credential):
        from src.presentation.schemas.notifications import ChangedCategoryStatus
        user = await self.token_service.get_user_by_token(jwt_token)
        changed_category = await self.notifications_repository.update_notifications_status(update_notification_data, category, user.id, get_notification_credential)
        result_data = ChangedCategoryStatus(category_id=changed_category.category_id, is_active=changed_category.is_active)
        return result_data

    async def stop_notification(self, registration_token, user_id):
        await self.notifications_repository.stop_notification(registration_token, user_id)

    async def get_notifications_status(self, registration_token, user_id):
        notifications_status = await self.notifications_repository.return_all_notification_objects_per_registration_token(registration_token, user_id)
        return notifications_status


    async def get_notification_by_user_id(self, user_id):
        notification_obj = await self.notifications_repository.get_notification_by_user_id(user_id=user_id)
        return notification_obj



    async def notificate_throw_token(self, category_title, article_title, article_author, tokens):

        for token in tokens:
        # messaging.Notification
            message = messaging.Message(
            notification=messaging.Notification(
                title=f"TDG: {category_title}",
                body=f"{article_author}: {article_title}"
            ),
            token=token,
        )

            response = messaging.send(message)






    # async def notificate_throw_topic(self, topic, message):
    #     print('=============NOTIFICATION TOPIC=================')
    #     print(topic)
    #     print(message)
    #     print('================================================')

    #     # cred = credentials.Certificate("./serviceAccountKey.json")
    #     # firebase_admin.initialize_app(cred)
    #     # See documentation on defining a message payload.
    #     message = messaging.Message(
    #         data={
    #             'message': message,
    #         },
    #         topic=topic,
    #     )

    #     # Send a message to the devices subscribed to the provided topic.
    #     response = messaging.send(message)
    #     # Response is a message ID string.
    #     print('Successfully sent message:', response)