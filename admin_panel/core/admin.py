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
from django import forms




from django.urls import path


from core.models import ArticlesUnfold, \
                        ArticleSectionsWithPlainTextUnfold, \
                        ArticleSectionWithSlideShowUnfold, \
                        ArticleSectionWithVideoUnfold, \
                        CategoryUnfold


# @admin.register(Articles)
# class ArticlesAdminClass(ModelAdmin):

#     compressed_fields = True  # Default: False


# @admin.register(ArticleSectionsWithPlainTextUnfold)
# class ArticleSectionsWithPlainTextAdminClass(ModelAdmin):
#     compressed_fields = True



# @admin.register(ArticleSectionWithSlideShowUnfold)
# class ArticleSectionWithSlideShowAdminClass(ModelAdmin):
#     compressed_fields = True



# @admin.register(ArticleSectionWithVideoUnfold)
# class ArticleSectionWithVideoAdminClass(ModelAdmin):
#     compressed_fields = True


@admin.register(CategoryUnfold)
class CategoryAdminClass(ModelAdmin):
    compressed_fields = True




class ArticleSectionsWithPlainTextInline(StackedInline):
    model = ArticleSectionsWithPlainTextUnfold
    extra = 1
    # exclude = ['id']
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
        # Здесь можно добавить обработку файлов
    def save(self, commit=True):
        instance = super().save(commit=False)
        print(self.cleaned_data)
        print('--->custom file saving<----')

        # Если нужно обработать файлы, можно сделать это здесь
        # Например, если у тебя в модели будет поле для файлов
        # if self.cleaned_data['file_field']:
        #     file_data = self.cleaned_data['file_field']
        #     instance.file_field = json.dumps({
        #         'filename': file_data.name,
        #         'size': file_data.size,
        #         'content_type': file_data.content_type,
        #     })

        if commit:
            instance.save()
        return instance

from django import forms
# =============================================================================>>>
class ArticleSectionWithSlideShowForm(forms.ModelForm):
    class Meta:
        model = ArticleSectionsWithPlainTextUnfold
        fields = '__all__'
        exclude = ["id"]
        formfield_overrides = {
        # models.ImageField: {
        #     "widget": forms.ImageField(),
        # }
    }
        
    # Здесь можно добавить обработку файлов
    def save(self, commit=True):
        instance = super().save(commit=False)
        print(self.cleaned_data)
        print('--->custom file saving<----')

        # Если нужно обработать файлы, можно сделать это здесь
        # Например, если у тебя в модели будет поле для файлов
        # if self.cleaned_data['file_field']:
        #     file_data = self.cleaned_data['file_field']
        #     instance.file_field = json.dumps({
        #         'filename': file_data.name,
        #         'size': file_data.size,
        #         'content_type': file_data.content_type,
        #     })

        if commit:
            instance.save()
        return instance
# ------------------------------------------------------------------------------///





class ArticleSectionWithSlideShowInline(StackedInline):
    model = ArticleSectionWithSlideShowUnfold
    form = ArticleSectionWithSlideShowForm
    extra = 1

    exclude = ["id"]
    # formfield_overrides = {
    #     models.TextField: {
    #         "widget": WysiwygWidget,
    #     }
    # }

class AArticleSectionWithVideoInline(TabularInline):
    model = ArticleSectionWithVideoUnfold
    extra = 1
    exclude = ["id"]

@admin.register(ArticlesUnfold)
class ArticlesAdmin(ModelAdmin):
    compressed_fields = True
    inlines = [ArticleSectionsWithPlainTextInline, ArticleSectionWithSlideShowInline, AArticleSectionWithVideoInline]

    



    # def get_urls(self):
    #     # Получаем стандартные пути Unfold
    #     urls = super().get_urls()

    #     custom_urls = [
    #         path('<int:pk>/change/', self.admin_site.admin_view(ArticleUpdateView.as_view()), name='article_change'),
    #         path('add/', self.admin_site.admin_view(ArticleCreateView.as_view()), name='article_add'),
    #     ]

    #     return custom_urls + urls