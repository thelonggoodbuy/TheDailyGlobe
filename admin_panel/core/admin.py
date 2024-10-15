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

from unfold.contrib.inlines.admin import NonrelatedStackedInline


from django.urls import path


# from admin_panel.core.models import ArticlesUnfold, \
#                         ArticleSectionsWithPlainTextUnfold, \
#                         ArticleSectionWithSlideShowUnfold, \
#                         ArticleSectionWithVideoUnfold, \
#                         CategoryUnfold


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
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def get_form_queryset(self, obj):
        return self.model.objects.all().distinct()

    def save_new_instance(self, parent, instance):
        last_obj = self.model.objects.order_by('id').last()
        next_id = last_obj.id + 1 if last_obj else 1
        instance.id = next_id
        print('=================================')


from django import forms
# =============================================================================>>>
# class ArticleSectionWithSlideShowForm(forms.ModelForm):
#     class Meta:
#         model = ArticleSectionsWithPlainTextUnfold
#         fields = '__all__'
#         exclude = ["id"]
#         formfield_overrides = {
#         # models.ImageField: {
#         #     "widget": forms.ImageField(),
#         # }
#     }
        
#     # Здесь можно добавить обработку файлов
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         print(self.cleaned_data)
#         print('--->custom file saving<----')

#         # Если нужно обработать файлы, можно сделать это здесь
#         # Например, если у тебя в модели будет поле для файлов
#         # if self.cleaned_data['file_field']:
#         #     file_data = self.cleaned_data['file_field']
#         #     instance.file_field = json.dumps({
#         #         'filename': file_data.name,
#         #         'size': file_data.size,
#         #         'content_type': file_data.content_type,
#         #     })

#         if commit:
#             instance.save()
#         return instance
# ------------------------------------------------------------------------------///





class ArticleSectionWithSlideShowInline(NonrelatedStackedInline):
    model = ArticleSectionWithSlideShowUnfold
    extra = 1

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def get_form_queryset(self, obj):
        return self.model.objects.all().distinct()

    def save_new_instance(self, parent, instance):
        last_obj = self.model.objects.order_by('id').last()
        next_id = last_obj.id + 1 if last_obj else 1
        instance.id = next_id
        print('=================================')

class ArticleSectionWithVideoInline(NonrelatedStackedInline):
    model = ArticleSectionWithVideoUnfold
    extra = 1
    
    def get_form_queryset(self, obj):
        return self.model.objects.all().distinct()

    def save_new_instance(self, parent, instance):
        last_obj = self.model.objects.order_by('id').last()
        next_id = last_obj.id + 1 if last_obj else 1
        instance.id = next_id
        print('=================================')


@admin.register(ArticlesUnfold)
class ArticlesAdmin(ModelAdmin):
    compressed_fields = True
    inlines = [ArticleSectionsWithPlainTextInline, ArticleSectionWithSlideShowInline, ArticleSectionWithVideoInline]

    



    # def get_urls(self):
    #     # Получаем стандартные пути Unfold
    #     urls = super().get_urls()

    #     custom_urls = [
    #         path('<int:pk>/change/', self.admin_site.admin_view(ArticleUpdateView.as_view()), name='article_change'),
    #         path('add/', self.admin_site.admin_view(ArticleCreateView.as_view()), name='article_add'),
    #     ]

    #     return custom_urls + urls