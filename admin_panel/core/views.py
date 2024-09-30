# from django.shortcuts import render
# from unfold.views import UnfoldModelAdminViewMixin
# from django.views.generic import TemplateView
# from .models import Articles
# from django.urls import reverse_lazy
# from django.views.generic.edit import UpdateView, CreateView
# from unfold.views import UnfoldModelAdminViewMixin


# class ArticleUpdateView(UpdateView, UnfoldModelAdminViewMixin):
#     model = Articles
#     title = "Update Article New title"  # required: custom page header title
#     permission_required = () # required: tuple of permissions
#     fields = ['title', 'category', 'lead', 'author', 'publication_date']
#     template_name = 'unfold/articles/change_form.html'
#     success_url = reverse_lazy('admin:core_articles_changelist')

#     def form_valid(self, form):
#         return super().form_valid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['opts'] = self.model._meta  # Передаем метаданные модели
#         # context['site'] = site              # Передаем объект админки
#         return context
    

# class ArticleCreateView(CreateView):
#     model = Articles
#     fields = ['title', 'category', 'lead', 'author', 'publication_date']
#     template_name = 'unfold/articles/create_form.html'
#     success_url = reverse_lazy('admin:core_articles_changelist')