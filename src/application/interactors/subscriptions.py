from urllib.parse import parse_qs, urlencode

from fastapi import Request
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.main.config.settings import Settings
from liqpay_lib.liqpay import LiqPay
import hashlib
import os



class SendPaymentRequestInteractor():
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

    async def __call__(self, token):
        # total_categories = await self.category_repository.get_all()
        # notification_statuses = await self.notification_service.get_notifications_status(registration_token_data.registration_token)


        liqpay = LiqPay(self.settings.payment_settings.LIQ_PAY_PUBLIC_KEY, self.settings.payment_settings.LIQ_PAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '1',
            'currency': 'UAH',
            'description': 'Payment for clothes',
            'order_id': hashlib.sha256(os.urandom(32)).hexdigest(),
            'version': '3',
            'sandbox': 1, # sandbox mode, set to 1 to enable it
            'server_url': 'https://tdg-admin.demodev.cc/receive_payment_callback', # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        print('============signature================')
        print(signature)
        print('=============data====================')
        print(data)
        print('=====================================')
        payment_url = f"https://www.liqpay.ua/api/3/checkout/?{urlencode({'data': data, 'signature': signature})}"
        return {"result": payment_url}
        # return {{'signature': signature, 'data': data}}
        # return render(request, self.template_name, {'signature': signature, 'data': data})


    # return {"result": "Success",
    #         "interactor": "SendPaymentRequestInteractor",
    #         "LIQ_PAY_PUBLIC_KEY": self.settings.payment_settings.LIQ_PAY_PUBLIC_KEY,
    #         "LIQ_PAY_PRIVATE_KEY": self.settings.payment_settings.LIQ_PAY_PRIVATE_KEY,}
    

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
