from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, ArticleCategory

# Create your views here.

def articles_list(request):
    a = Article.objects.all().order_by('-created_on')
    ctx = {
        'articles': a
    }
    return render(request, 'wiki/articles_list.html',ctx)

def article_detail(request, id):
    a = Article.objects.get(id=id)
    ctx = {
        'article': a
    }
    
    return render(request, 'wiki/article_detail.html', ctx)

