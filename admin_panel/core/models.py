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
import json
import uuid


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class ArticleSectionWithSlideShowUnfold(models.Model):
    # id = models.IntegerField(primary_key=True)
    # id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="galery/")
    article = models.ForeignKey('ArticlesUnfold', models.DO_NOTHING, blank=True, null=True)
    text = models.TextField()
    intex_number_in_article = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'article_section_with_slide_show'


    
class ArticleSectionWithVideoUnfold(models.Model):
    # id = models.IntegerField(primary_key=True)
    # id = models.AutoField(primary_key=True)
    video_url = models.CharField(max_length=255)
    article = models.ForeignKey('ArticlesUnfold', models.DO_NOTHING, blank=True, null=True)
    text = models.TextField()
    intex_number_in_article = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'article_section_with_video'


class ArticleSectionsWithPlainTextUnfold(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)

    
    article = models.ForeignKey('ArticlesUnfold', models.DO_NOTHING, blank=True, null=True)
    text = models.TextField()
    intex_number_in_article = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'article_sections_with_plain_text'


class ArticlesUnfold(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('CategoryUnfold', models.DO_NOTHING, blank=True, null=True)
    lead = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255)
    publication_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'articles'

    def __str__(self):
        return f'{self.title}: {self.author}'


class CategoryUnfold(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
        return f'{self.title}'


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
    subscription_type = models.TextField()  # This field type is a guess.

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
