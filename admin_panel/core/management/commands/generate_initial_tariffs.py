from decimal import Decimal
from django.core.management.base import BaseCommand

from admin_panel.core.models import CurrencyType, TariffUnfold, TimePeriod


class Command(BaseCommand):
    help = "Ініціалізація тестових категорій тарифів"

    def handle(self, *args, **kwargs):
        how_many_tariff = TariffUnfold.objects.count()
        if how_many_tariff < 1:
            print("В системі не знайдено жодного таріфу...")
            print("Створюємо...")
            new_tariff = TariffUnfold.objects.create(
                title="Quick start",
                cost=Decimal("5.00"),
                cost_per_year=Decimal("260.00"),
                subscription_period=TimePeriod.WEEK,
                curency=CurrencyType.USD
            )
            print(f"Таріф {new_tariff.title} створено...")

            new_tariff = TariffUnfold.objects.create(
                title="Basic plan",
                cost=Decimal("15.00"),
                cost_per_year=Decimal("180.00"),
                subscription_period=TimePeriod.MONTH,
                curency=CurrencyType.USD
            )
            print(f"Таріф {new_tariff.title} створено...")

            new_tariff = TariffUnfold.objects.create(
                title="Advanced plan",
                cost=Decimal("150.00"),
                subscription_period=TimePeriod.YEAR,
                curency=CurrencyType.USD
            )
            print(f"Таріф {new_tariff.title} створено...")
        else:
            print('В системі вже є тарифи...')


        # obj, created = CategoryUnfold.objects.get_or_create(
        #     title='культура',
        #     extended_title='Останні новини культури',
        # )
        # if created: print("Категорія 'культура' створена...")

        # obj, created = CategoryUnfold.objects.get_or_create(
        #     title='технології',
        #     extended_title='Останні новини технологій',
        # )
        # if created: print("Категорія 'технології' створена...")

        # total_categories = CategoryUnfold.objects.all()
        # print("В системі збережені є такі категорії:")
        # for category in total_categories:
        #     print(category)