from fastapi import APIRouter, Request
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject
from typing import Annotated
from fastapi import Depends
from src.application.interactors.subscriptions import ReceivePaymentRequestInteractor, SendPaymentRequestInteractor
from src.infrastructure.openapi.openapi import bearer_scheme




router = APIRouter(route_class=DishkaRoute)


@router.post("/send_payment_request", tags=["subscriptions"])
@inject
async def send_payment_request(token: Annotated[str, Depends(bearer_scheme)],
                                    interactor: FromDishka[SendPaymentRequestInteractor]):
    result = await interactor(token.credentials)
    return result



@router.post("/receive_payment_callback", tags=["subscriptions"])
@inject
async def receive_payment_callback(request: Request, 
                                    interactor: FromDishka[ReceivePaymentRequestInteractor]):
    result = await interactor(request)
    return result