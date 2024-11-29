from django.core.management.base import BaseCommand

# from django.core.management.base import BaseCommand
# import random


from admin_panel.core.models import ArticlesUnfold,\
                                    CategoryUnfold,\
                                    ArticleSectionsWithPlainTextUnfold,\
                                    ArticleSectionWithSlideShowUnfold,\
                                    ArticleSectionWithVideoUnfold
# from django.contrib.auth import User
import random
from datetime import datetime, timedelta
import os

from django.core.files import File


from faker import Faker

fake = Faker("uk_UA")
fake_ru = Faker("ru")


from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ініціалізація тестових категорій"

    def handle(self, *args, **kwargs):

        all_articles_len = len(ArticlesUnfold.objects.all())
        print('++++++++++++++++++++')
        print(all_articles_len)
        print('++++++++++++++++++++')
        if all_articles_len < 3: 
            print("В системі меньше трьох статей. Генеруємо")
            self.generate_articles()

        # obj, created = CategoryUnfold.objects.get_or_create(
        #     title='екоміка',
        # )
        # if created: print("Категорія 'економіка' створена...")

        # obj, created = CategoryUnfold.objects.get_or_create(
        #     title='культура',
        # )
        # if created: print("Категорія 'культура' створена...")

        # obj, created = CategoryUnfold.objects.get_or_create(
        #     title='технології',
        # )
        # if created: print("Категорія 'технології' створена...")

        # total_categories = CategoryUnfold.objects.all()
        # print("В системі збережені є такі категорії:")
        # for category in total_categories:
        #     print(category)

    def generate_articles(self):
        categories = CategoryUnfold.objects.all()
        for category in categories:
            self.generate_article_per_category(category)

    def generate_article_per_category(self, category):
        for i in range(1,12):
            article = ArticlesUnfold(
                title=fake.sentence(nb_words=6),
                category=category,
                lead=fake.paragraph(nb_sentences=10),
                author=fake.name(),
                publication_date=self.generate_timestamp(),
                is_premium=random.choices([False, True], weights=[70, 30], k=1)[0],
                viewing=random.randint(1, 150)
            )
            random_image_path = self.get_random_image()
            with open(random_image_path, 'rb') as image_file:
                article.main_image.save(os.path.basename(random_image_path), File(image_file))
            article.save()
            self.generate_article_sections(article)
            print(f"Стаття {article} створена!")
            


    def generate_timestamp(self):
        now = datetime.now()

        # Date and time 1 week ago
        one_week_ago = now - timedelta(weeks=1)

        # Generate a random timestamp between one_week_ago and now
        random_timestamp = one_week_ago + (now - one_week_ago) * random.random()
        return random_timestamp
    
    def generate_article_sections(self, article):
        for i in [0, 1, 2, 3, 4, 6, 8, 10, 11]:
            section_with_plain_text = ArticleSectionsWithPlainTextUnfold(
                article=article,
                text=fake.paragraph(nb_sentences=10),
                index_number_in_article=i
            )
            section_with_plain_text.save()

        for i in [2, 5, 9]:
            author_of_photos = fake.name()
            random_image_path = self.get_random_image()
            with open(random_image_path, 'rb') as image_file:
                article_section_with_slide_show_unfold = ArticleSectionWithSlideShowUnfold(
                    article=article,
                    text=fake.paragraph(nb_sentences=10),
                    index_number_in_article=i,
                    author=author_of_photos
                )
                article_section_with_slide_show_unfold.image.save(os.path.basename(random_image_path), File(image_file))
                article_section_with_slide_show_unfold.save()
        
        for i in [7, 11]:
            random_image_path = self.get_random_image()
            with open(random_image_path, 'rb') as image_file:
                article_section_with_video_unfold = ArticleSectionWithVideoUnfold(
                    video_url='https://youtu.be/wm_RTOABNKs?si=hnLAj5nM8moBSFcX',
                    article=article,
                    text=fake.paragraph(nb_sentences=2),
                    title=fake.paragraph(nb_sentences=1),
                    index_number_in_article=i,
                )
                article_section_with_video_unfold.image_preview.save(os.path.basename(random_image_path), File(image_file))
                article_section_with_video_unfold.save()


    def get_random_image(self):
        folder_path="seed/image"
        # List all files in the folder
        files = os.listdir(folder_path)
        
        # Filter to include only image files
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        # Check if there are any image files
        if not image_files:
            raise FileNotFoundError("No image files found in the folder.")
        
        # Select a random image file
        random_image = random.choice(image_files)
        
        # Return the full path to the image
        return os.path.join(folder_path, random_image)

        