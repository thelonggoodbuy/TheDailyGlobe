from src.infrastructure.celery_app.celery_app import celery_app
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials
import json



@celery_app.task
def send_notification(category_title, article_title, article_author, article_id, tokens):
    
    # TODO: add to .env
    cred = credentials.Certificate("./serviceAccountKey.json")
    data_payload = json.dumps({"articleId": str(article_id)})

    try:
        firebase_app = firebase_admin.get_app(name="firebase_app")
    except ValueError:
        firebase_app = firebase_admin.initialize_app(cred, name="firebase_app")

    for token in tokens:
        # messaging.Notification
        message = messaging.Message(
        data={"payload": data_payload},
        notification=messaging.Notification(
            title=f"TDG: {category_title}",
            body=f"{article_author}: {article_title}"
        ),
        token=token,
    )

        response = messaging.send(message, app=firebase_app)


@celery_app.task
def send_success_notification(user_email, subscription_exp_date, registration_token):


    cred = credentials.Certificate("./serviceAccountKey.json")
    # data_payload = json.dumps({"articleId": str(article_id)})

    try:
        firebase_app = firebase_admin.get_app(name="firebase_app")
    except ValueError:
        firebase_app = firebase_admin.initialize_app(cred, name="firebase_app")

    message = messaging.Message(
        # data={"payload": data_payload},
        notification=messaging.Notification(
            title=f"TDG: дякуємо за підтримку, {user_email}",
            body=f"Ваша підписка продлонгована до {subscription_exp_date}."
        ),
        token=registration_token,
    )

    response = messaging.send(message, app=firebase_app)
    print('data in response:***')
    print(response)
    print('********************')
    print('send notification task from liqpay callback work and create or use firebase app!')