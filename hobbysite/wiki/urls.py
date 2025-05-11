"""Route app URL's."""

from django.urls import path
from .views import articles_list, article_detail, article_create, article_update

urlpatterns = [
        path('articles/', articles_list, name='index'),
        path('article/<int:id>/', article_detail, name='article_detail'),
        path('article/<int:id>/edit', article_update, name='article_update'),
        path('article/add/', article_create, name='article_create')
    ]

app_name = "wiki"
