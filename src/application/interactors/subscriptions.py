from src.infrastructure.interfaces.uow import IDatabaseSession
from src.main.config.settings import Settings
from liqpay import LiqPay




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
            'currency': 'GRN',
            'description': 'Payment for clothes',
            'order_id': 'order_id_1',
            'version': '3',
            'sandbox': 1, # sandbox mode, set to 1 to enable it
            'server_url': 'https://tdg-admin.demodev.cc/receive_payment_callback/', # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        print('============signature================')
        print(signature)
        print('=============data====================')
        print(data)
        print('=====================================')
        return {{'signature': signature, 'data': data}}
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

    async def __call__(self, token):
        # total_categories = await self.category_repository.get_all()
        # notification_statuses = await self.notification_service.get_notifications_status(registration_token_data.registration_token)
        return {"result": "Success", "interactor": "ReceivePaymentRequestInteractor"}