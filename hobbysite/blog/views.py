from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleCategory

def article_list(request):
    categories = ArticleCategory.objects.all()
    return render(request, 'article_list.html', {'categories': categories})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})