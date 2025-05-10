"""This file contains the views for the blog app."""
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Article, ArticleCategory, Comment
from .forms import CommentForm
from user_management.models import Profile


def article_list(request):
    """Display a list of articles."""
    categories = ArticleCategory.objects.all()
    user_articles = None
    all_articles = None
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        user_articles = Article.objects.filter(author=current_user).order_by('-created_on')
        all_articles = Article.objects.exclude(author=current_user).order_by('-created_on')
    else:
        all_articles = Article.objects.all().order_by('-created_on')

    return render(request, 'article_list.html', {
        'categories': categories,
        'user_articles': user_articles, 
        'all_articles': all_articles,
    })


def article_detail(request, id):
    """Display a single article."""
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all().order_by('-created_on')
    related_articles = Article.objects.filter(author=article.author).exclude(id=article.id)[:2]
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = Profile.objects.get(user=request.user)
            comment.article = article
            comment.save()
            return HttpResponseRedirect(reverse('article_detail', args=[id]))
    else:
        form = CommentForm() if request.user.is_authenticated else None
    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
        'form': form,
    })
