"""Route app URL's."""

from django.urls import path
from .views import articles_list, article_detail

urlpatterns = [
        path('articles/', articles_list, name='articles_list'),
        path('article/<int:id>/', article_detail, name='article_detail')
    ]

app_name = "wiki"
