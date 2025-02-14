from urllib.parse import parse_qs, urlencode

from fastapi import Request
from fastapi.responses import JSONResponse
from src.application.interfaces.services import ITokenService
from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.application.interfaces.repositories import BaseSubscribtionRepository, BaseTariffRepository, BaseTransactionsRepository
from src.presentation.schemas.subscriptions import AllTariffResponseSchema
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.main.config.settings import Settings
from liqpay_lib.liqpay import LiqPay
import hashlib
import os



class SendPaymentRequestInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        subscription_repository: BaseSubscribtionRepository,
        transaction_repository: BaseTransactionsRepository,
        tariff_repository: BaseTariffRepository,
        token_service: ITokenService,
        settings: Settings):

        self.db_session = db_session
        self.token_service = token_service
        self.subscription_repository = subscription_repository
        self.transaction_repository = transaction_repository
        self.tariff_repository = tariff_repository
        self.settings = settings

    async def __call__(self, token, tariff_id):

        # 1 extract user throw token
        user_obj = await self.token_service.get_user_by_token(token)
        if not user_obj.is_valid:
            result = BaseResponseSchema(
                error=True,
                message=user_obj.error_text,
                data=None
            )
            return JSONResponse(status_code=401, content=result.model_dump())
        
        # 2 extract subscription obj
        subscription_obj = await self.subscription_repository.return_user_subscribtion_by_user_id(user_id=user_obj.id)
        if not subscription_obj:
            subscription_obj = await self.subscription_repository.create_subscription(user_id=user_obj.id)

        # 3 extract tariff
        tariff = await self.tariff_repository.return_tariff_by_id(tariff_id=tariff_id)

        # print('==========extracted data=============')
        # print(subscription_obj)
        # print(user_obj)
        # print(tariff)
        # print('=====================================')

        # 4 create transaction object
        print('==========extracted data=============')
        print(subscription_obj)
        print(user_obj)
        print(tariff)
        print('=====================================')
        subscription_obj = await self.subscription_repository.return_user_subscribtion_by_user_id(user_obj.id)
        new_transaction = await self.transaction_repository.create_transaction(subscription_obj.id)
        await self.transaction_repository.print_all_transaction()


        liqpay = LiqPay(self.settings.payment_settings.LIQ_PAY_PUBLIC_KEY, self.settings.payment_settings.LIQ_PAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': float(tariff.cost),
            'currency': str(tariff.curency.value),
            'description': f'TDG: payment for subscription for {tariff.subscription_period}',
            'order_id': new_transaction.order_id,
            'version': '3',
            'sandbox': 1, # sandbox mode, set to 1 to enable it
            'server_url': 'https://tdg-admin.demodev.cc/receive_payment_callback', # url to callback view
        }
        # params = {
        #     'action': 'pay',
        #     'amount': '1',
        #     'currency': 'UAH',
        #     'description': 'Payment for clothes',
        #     'order_id': hashlib.sha256(os.urandom(32)).hexdigest(),
        #     'version': '3',
        #     'sandbox': 1, # sandbox mode, set to 1 to enable it
        #     'server_url': 'https://tdg-admin.demodev.cc/receive_payment_callback', # url to callback view
        # }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        payment_url = f"https://www.liqpay.ua/api/3/checkout/?{urlencode({'data': data, 'signature': signature})}"


        # return {"result": payment_url}
    
        # return {"result": "success"}
        

class ReceivePaymentRequestInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        # notification_service: INotificationService,
        # category_repository: BaseCategoryRepository, 
        # token_service: ITokenService,
        settings: Settings):

        self.db_session = db_session
        # self.notification_service = notification_service
        # self.category_repository = category_repository
        # self.token_service = token_service
        self.settings = settings

    async def __call__(self, request: Request):
        # total_categories = await self.category_repository.get_all()
        # notification_statuses = await self.notification_service.get_notifications_status(registration_token_data.registration_token)
        print('================***YOU HAVE RECEIVE MESSAGE***================')
        liqpay = LiqPay(self.settings.payment_settings.LIQ_PAY_PUBLIC_KEY, self.settings.payment_settings.LIQ_PAY_PRIVATE_KEY)
        raw_body = await request.body()
        parsed_data = parse_qs(raw_body.decode("utf-8"))

        data = parsed_data.get("data", [""])[0]
        signature = parsed_data.get("signature", [""])[0]

        
        print('request data:')
        print(request)
        print(request.json())
        print(await request.body())
        # data = request.POST.get('data')
        # signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(self.settings.payment_settings.LIQ_PAY_PUBLIC_KEY + data + self.settings.payment_settings.LIQ_PAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)
        print({"result": "Success", "interactor": "ReceivePaymentRequestInteractor"})



class ReturnAllTariffsInteractor():
    def __init__(self,
        db_session: IDatabaseSession,
        tariff_repository: BaseTariffRepository, 
        settings: Settings):

        self.db_session = db_session
        self.tariff_repository = tariff_repository
        self.settings = settings

    async def __call__(self):
        all_tariffs = await self.tariff_repository.return_all()
        result = AllTariffResponseSchema(tariff_list=all_tariffs)
        return result