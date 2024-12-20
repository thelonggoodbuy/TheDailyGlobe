from src.application.interfaces.services import INotificationService
from src.main.config.settings import Settings
import firebase_admin
from firebase_admin import credentials, messaging


class NotificationFirebaseService(INotificationService):
    """ Service for notification throw firebase """

    def __init__(
        self,
        settings: Settings
    ):
        # """Initialize Jwt token settings."""
        self.settings = settings

        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)


    async def notificate_throw_token(self, registration_token, message_text):


        print('=============NOTIFICATION TOKEN=================')
        print(registration_token)
        print(message_text)
        print('================================================')


        
        message = messaging.Message(
            data={
                'message_text': message_text
            },
            token=registration_token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)

        # if response.failure_count > 0:
        #     print(f"Failed to send {response.failure_count} messages: {response.responses}")
        # Response is a message ID string.
        print('Successfully sent message:', response)





    async def notificate_throw_topic(self, topic, message):
        print('=============NOTIFICATION TOPIC=================')
        print(topic)
        print(message)
        print('================================================')

        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        # See documentation on defining a message payload.
        message = messaging.Message(
            data={
                'message': message,
            },
            topic=topic,
        )

        # Send a message to the devices subscribed to the provided topic.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)