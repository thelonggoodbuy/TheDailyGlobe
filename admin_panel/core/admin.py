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
from django.db.models import Count

from unfold.admin import StackedInline, TabularInline

from django import forms

from unfold.contrib.inlines.admin import NonrelatedStackedInline


from django.urls import path

from admin_panel.core.models import ArticlesUnfold, \
                        ArticleSectionsWithPlainTextUnfold, \
                        ArticleSectionWithSlideShowUnfold, \
                        ArticleSectionWithVideoUnfold, \
                        CategoryUnfold, UsersUnfold


from unfold.contrib.filters.admin import TextFilter, FieldTextFilter
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter, RangeNumericFilter
from django.contrib.admin.filters import ChoicesFieldListFilter





@admin.register(CategoryUnfold)
class CategoryAdminClass(ModelAdmin):
    compressed_fields = True




class ArticleSectionsWithPlainTextInline(StackedInline):
    model = ArticleSectionsWithPlainTextUnfold
    extra = 1
    exclude = ['section_type',]




class ArticleSectionWithSlideShowInline(StackedInline):
    model = ArticleSectionWithSlideShowUnfold
    extra = 1
    exclude = ['section_type',]


class ArticleSectionWithVideoInline(StackedInline):
    model = ArticleSectionWithVideoUnfold
    extra = 1
    exclude = ['section_type',]



class HorizontalChoicesFieldListFilter(ChoicesFieldListFilter):
    horizontal = True


@admin.register(ArticlesUnfold)
class ArticlesAdmin(ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_premium",

    )
    list_filter = ("is_premium", 
                   ("publication_date", RangeDateFilter), 
                   ("id", RangeNumericFilter),
                   "author",)
    search_fields = ("lead", "author",)
    

    inlines = [ArticleSectionsWithPlainTextInline, ArticleSectionWithSlideShowInline, ArticleSectionWithVideoInline]


@admin.register(UsersUnfold)
class ArticlesAdmin(ModelAdmin):
    model = UsersUnfold
    extra = 1


    
