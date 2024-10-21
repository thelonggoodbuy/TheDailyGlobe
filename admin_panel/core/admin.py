from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
# from django.db import models
from unfold.admin import ModelAdmin
# from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline
# from .views import ArticleUpdateView, ArticleCreateView
from unfold.contrib.forms.widgets import WysiwygWidget
from ckeditor.widgets import CKEditorWidget


from django import forms

from unfold.contrib.inlines.admin import NonrelatedStackedInline


from django.urls import path

from admin_panel.core.models import ArticlesUnfold, \
                        ArticleSectionsWithPlainTextUnfold, \
                        ArticleSectionWithSlideShowUnfold, \
                        ArticleSectionWithVideoUnfold, \
                        CategoryUnfold



@admin.register(CategoryUnfold)
class CategoryAdminClass(ModelAdmin):
    compressed_fields = True




class ArticleSectionsWithPlainTextInline(NonrelatedStackedInline):
    model = ArticleSectionsWithPlainTextUnfold
    extra = 1
    exclude = ['article', ]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def get_form_queryset(self, obj):
        return self.model.objects.filter(article_id=obj.id).distinct()

    def save_new_instance(self, parent, instance):
        last_obj = self.model.objects.order_by('id').last()
        next_id = last_obj.id + 1 if last_obj else 1
        instance.id = next_id
        instance.article_id = parent.id




class ArticleSectionWithSlideShowInline(NonrelatedStackedInline):
    model = ArticleSectionWithSlideShowUnfold
    extra = 1
    exclude = ['article', ]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def get_form_queryset(self, obj):
        return self.model.objects.filter(article_id=obj.id).distinct()

    def save_new_instance(self, parent, instance):
        last_obj = self.model.objects.order_by('id').last()
        next_id = last_obj.id + 1 if last_obj else 1
        instance.id = next_id
        instance.article_id = parent.id


class ArticleSectionWithVideoInline(NonrelatedStackedInline):
    model = ArticleSectionWithVideoUnfold
    extra = 1
    exclude = ['article', ]
    
    def get_form_queryset(self, obj):
        return self.model.objects.filter(article_id=obj.id).distinct()

    def save_new_instance(self, parent, instance):
        last_obj = self.model.objects.order_by('id').last()
        next_id = last_obj.id + 1 if last_obj else 1
        instance.id = next_id
        instance.article_id = parent.id



@admin.register(ArticlesUnfold)
class ArticlesAdmin(ModelAdmin):
    compressed_fields = True
    # inlines = [ArticleSectionsWithPlainTextInline,]
    # formfield_overrides = {
    #         models.TextField: {
    #             "widget": WysiwygWidget,
    #         }
    #     }
    inlines = [ArticleSectionsWithPlainTextInline, ArticleSectionWithSlideShowInline, ArticleSectionWithVideoInline]
    
