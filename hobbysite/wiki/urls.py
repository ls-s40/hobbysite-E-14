"""Route app URL's."""

from django.urls import path
from .views import articles_list, article_detail, article_create

urlpatterns = [
        path('articles/', articles_list, name='index'),
        path('article/<int:id>/', article_detail, name='article_detail'),
        path('article/add/', article_create, name='article_create')
    ]

app_name = "wiki"
