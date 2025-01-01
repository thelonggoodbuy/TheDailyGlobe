from django.core.management.base import BaseCommand

# from django.core.management.base import BaseCommand
# import random


# from admin_panel.core.models import User, Role
# from django.contrib.auth import User


# from faker import Faker

# fake = Faker("ru")


from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Инициализация тестового пользователя"

    def handle(self, *args, **kwargs):
        print('*************************************************')
        print('***********this is testing command***************')
        print('***************all work!*************************')
        print('*************************************************')
        User = get_user_model()
        username = "admin"
        email = "admin@example.com"
        password = "some_password"
        is_staff = True
        is_superuser = True
        if not User.objects.filter(username=username).exists():

            admin = User.objects.create(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser)

            admin.set_password(password)
            admin.save()

            print(f"Superuser {username} created successfully!")
        else:
            print(f"Superuser {username} already exists.")

        all_users = User.objects.all()
        for user in all_users:
            print('=======================')
            print(f'User with id {user.id}')
            print((f'User with email {user.email}'))
            print((f'User with username {user.username}'))
            print('=======================')



#         test_users_query = User.objects.filter(email="initial_simple_user_1@email.com")
#         if test_users_query.exists():
#             print("*************************************************")
#             print("***********тестовые данные пользователей*********")
#             print("***************уже есть в базе данных************")
#             print("*************************************************")
#         else:
#             all_roles = Role.objects.exclude(name="Директор")

#             for index in range(1, 350):
#                 password = "Te5t_pasSword"
#                 if User.objects.filter(email=f"initial_simple_user_{index}@gmail.com"):
#                     continue
#                 else:
#                     email = f"initial_simple_user_{index}@gmail.com"
#                     fake_name = fake.name()
#                     fake_list = fake_name.split(" ")
#                     surname = fake_list[-1]
#                     name = fake_list[-2]
#                     patronymic = "Григорьевич"
#                     is_active = random.choice([True, False])
#                     # is_superuser = random.choice([True, False])
#                     is_superuser = False
#                     # is_staff = random.choice([True, False])
#                     is_staff = False
#                     note = fake.text()
#                     phone = "0637149378"
#                     is_role = random.choice([True, False])
#                     role = None
#                     if is_role == True:
#                         role = random.choice(all_roles)
#                     status = random.choice(("active", "new", "disable"))
#                     user = User(
#                         email=email,
#                         surname=surname,
#                         name=name,
#                         patronymic=patronymic,
#                         is_active=is_active,
#                         is_superuser=is_superuser,
#                         is_staff=is_staff,
#                         note=note,
#                         phone=phone,
#                     )
#                     if role != None:
#                         user.role = role
#                     user.status = status
#                     user.set_password(password)
#                     user.save()