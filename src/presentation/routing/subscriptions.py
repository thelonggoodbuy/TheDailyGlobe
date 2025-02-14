from fastapi import APIRouter, Request
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject
from typing import Annotated
from fastapi import Depends
from src.presentation.schemas.subscriptions import TariffRequestSchema
from src.application.interactors.subscriptions import ReceivePaymentRequestInteractor, ReturnAllTariffsInteractor, SendPaymentRequestInteractor
from src.infrastructure.openapi.openapi import bearer_scheme




router = APIRouter(route_class=DishkaRoute)


@router.post("/send_payment_request", tags=["subscriptions"])
@inject
async def send_payment_request(token: Annotated[str, Depends(bearer_scheme)],
                               tariff: TariffRequestSchema,
                                interactor: FromDishka[SendPaymentRequestInteractor]):
    result = await interactor(token.credentials, tariff.tariff_id)
    return result



@router.post("/receive_payment_callback", tags=["subscriptions"])
@inject
async def receive_payment_callback(request: Request, 
                                    interactor: FromDishka[ReceivePaymentRequestInteractor]):
    result = await interactor(request)
    return result


@router.get("/return_all_tariffs", tags=["subscriptions"])
@inject
async def return_all_tariffs(interactor: FromDishka[ReturnAllTariffsInteractor]):
    result = await interactor()
    return result