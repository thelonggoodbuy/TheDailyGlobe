# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.files.storage import default_storage
from django.utils.timezone import now
from django.conf import settings
from src.application.tasks.notification_tasks import send_notification



class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class ArticleSectionWithSlideShowUnfold(models.Model):
    # id = models.IntegerField(primary_key=True)
    # id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="galery/")
    article = models.ForeignKey('ArticlesUnfold', models.CASCADE, blank=True, null=True)
    text = models.TextField()
    index_number_in_article = models.IntegerField()
    section_type = models.CharField(max_length=50, default='article_section_with_slide_show', null=False)
    author = models.CharField(max_length=255)


    class Meta:
        managed = False
        db_table = 'article_section_with_slide_show'


    
class ArticleSectionWithVideoUnfold(models.Model):
    # id = models.IntegerField(primary_key=True)
    # id = models.AutoField(primary_key=True)
    video_url = models.CharField(max_length=255)
    article = models.ForeignKey('ArticlesUnfold', models.CASCADE, blank=True, null=True)
    text = models.TextField()
    index_number_in_article = models.IntegerField()
    section_type = models.CharField(max_length=50, default='article_section_with_video', null=False)
    title = models.CharField(max_length=255)
    image_preview = models.ImageField(upload_to="galery/")

    class Meta:
        managed = False
        db_table = 'article_section_with_video'


class ArticleSectionsWithPlainTextUnfold(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey('ArticlesUnfold', models.CASCADE, blank=True, null=True)
    text = models.TextField()
    index_number_in_article = models.IntegerField()
    section_type = models.CharField(max_length=50, default='article_sections_with_plain_text', null=False)

    class Meta:
        managed = False
        db_table = 'article_sections_with_plain_text'


class ArticlesUnfold(models.Model):
    title = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to="galery/")
    category = models.ForeignKey('CategoryUnfold', models.DO_NOTHING, blank=True, null=True)
    lead = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255)
    publication_date = models.DateTimeField()
    viewing = models.IntegerField(default=0, blank=True, null=True)
    is_premium = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'articles'

    def __str__(self):
        return f'{self.title}: {self.author}'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tokens = list(NotificationCredentialUnfold.objects.filter(choosen_categories__id=self.category.id)
                                                    .values_list('registraion_token', flat=True))

        send_notification.delay(category_title=self.category.title,
                                article_title=self.title,
                                article_author=self.author, 
                                article_id = self.id,
                                tokens=tokens)

    



class CategoryUnfold(models.Model):
    title = models.CharField(max_length=255)
    extended_title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
        return f'{self.title}'




class NotificationCredentialUnfold(models.Model):
    id = models.AutoField(primary_key=True)
    registraion_token = models.CharField(max_length=255)
    user = models.ForeignKey('UsersUnfold', on_delete=models.CASCADE, null=True, blank=True)
    choosen_categories = models.ManyToManyField(CategoryUnfold, through='CategoryNotificationCredentialUnfold')

    class Meta:
        db_table = 'notification_credential'
        managed = False


class CategoryNotificationCredentialUnfold(models.Model):
    category = models.ForeignKey(CategoryUnfold, on_delete=models.CASCADE)
    notification_credential = models.ForeignKey(NotificationCredentialUnfold, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_notification_credetial'
        managed = False


class CommentsUnfold(models.Model):
    text = models.TextField(blank=True, null=True)
    article = models.ForeignKey(ArticlesUnfold, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class SearchRequestUnfold(models.Model):
    text = models.CharField(max_length=255)
    quantity_of_search_requests = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_request'


class SubscriptionsUnfold(models.Model):
    user = models.OneToOneField('UsersUnfold', models.DO_NOTHING, blank=True, null=True)
    expiration_date = models.DateTimeField()
    # subscription_type = models.TextField()  # This field type is a guess.
    registration_id = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'subscriptions'


class UnregisteredDevicesUnfold(models.Model):
    device_id = models.CharField(max_length=255)
    device_type = models.TextField()  # This field type is a guess.
    readed_articles = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unregistered_devices'


class UsersUnfold(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'
