from django.core.management.base import BaseCommand

# from django.core.management.base import BaseCommand
# import random


from admin_panel.core.models import CategoryUnfold
# from django.contrib.auth import User


# from faker import Faker

# fake = Faker("ru")


from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ініціалізація тестових категорій"

    def handle(self, *args, **kwargs):

        obj, created = CategoryUnfold.objects.get_or_create(
            title='екоміка',
        )
        if created: print("Категорія 'економіка' створена...")

        obj, created = CategoryUnfold.objects.get_or_create(
            title='культура',
        )
        if created: print("Категорія 'культура' створена...")

        obj, created = CategoryUnfold.objects.get_or_create(
            title='технології',
        )
        if created: print("Категорія 'технології' створена...")

        total_categories = CategoryUnfold.objects.all()
        print("В системі збережені є такі категорії:")
        for category in total_categories:
            print(category)