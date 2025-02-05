from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute


from src.application.interactors.notifications import TestNotificationThrowTokenInteractor,\
                                                    ReturnNotificationCredentialsInteractor,\
                                                    UpdateNotificationCredentialsInteractor,\
                                                    GetNotificationsStatusInteractor,\
                                                    UpdateNotificationsStatusInteractor


from src.presentation.schemas.notifications import SaveOrUpdateNotificationCredesRequestSchema,\
                                                SaveOrUpdateNotificationCredesResponseSchema,\
                                                NotificationCategoryStateObjectSchema,\
                                                ReturnNotificationsStateResponseSchema,\
                                                UpdateNotificationStateRequestSchema    

from fastapi import Depends

from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from typing import Annotated
from src.infrastructure.openapi.openapi import bearer_scheme



router = APIRouter(route_class=DishkaRoute)


@router.post("/save_notification_credentials", tags=["notification"])
@inject
async def save_notification_credentials(token: Annotated[str, Depends(bearer_scheme)],
                                            registration_token_data: SaveOrUpdateNotificationCredesRequestSchema, 
                                            interactor: FromDishka[ReturnNotificationCredentialsInteractor]):
    result = await interactor(token.credentials, registration_token_data.registration_token)
    return result


# !(2)
# @router.post("/update_notification_credentials", tags=["notification"])
# @inject
# async def update_notification_credentials(token: Annotated[str, Depends(bearer_scheme)], 
#                                             registration_token_data: SaveOrUpdateNotificationCredesRequestSchema,\
#                                             # interactor: FromDishka[UpdateNotificationCredentialsInteractor]) -> SaveOrUpdateNotificationCredesResponseSchema:
#                                             interactor: FromDishka[UpdateNotificationCredentialsInteractor]):
#     await interactor(token, registration_token_data)
#     return True


# # (3)
@router.post("/get_notifications_status", tags=["notification"])
@inject
async def get_notifications_status(token: Annotated[str, Depends(bearer_scheme)],
                                registration_token_data: SaveOrUpdateNotificationCredesRequestSchema,
                                interactor: FromDishka[GetNotificationsStatusInteractor]):
    result = await interactor(registration_token_data, token)
    return result

# # (4)
@router.post("/update_notifications_status", tags=["notification"])
async def update_notifications_status(token: Annotated[str, Depends(bearer_scheme)],
                                        update_notification_data: UpdateNotificationStateRequestSchema,
                                        interactor: FromDishka[UpdateNotificationsStatusInteractor]):
    
    result = await interactor(token, update_notification_data)
    return result