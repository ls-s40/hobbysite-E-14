"""This file contains the views for the blog app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Article, ArticleCategory, Comment
from user_management.models import Profile


def article_list(request):
    """Display a list of articles."""
    categories = ArticleCategory.objects.all()
    user_articles = None
    all_articles = None
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        user_articles = Article.objects.filter(
            author=current_user
            ).order_by('-created_on')
        all_articles = Article.objects.exclude(
            author=current_user
            ).order_by('-created_on')
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
    related_articles = Article.objects.filter(
        author=article.author
        ).exclude(id=article.id)[:2]

    if request.method == 'POST' and request.user.is_authenticated:
        entry = request.POST.get('entry')
        if entry:
            author = Profile.objects.get(user=request.user)
            Comment.objects.create(
                author=author,
                article=article,
                entry=entry
            )
            return HttpResponseRedirect(
                reverse('blog:article_detail', args=[id])
                )

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
    })


@login_required
def article_create(request):
    """Create a new article."""
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        entry = request.POST.get('entry')
        header_image = request.FILES.get('header_image')
        category = (ArticleCategory.objects.get(id=category_id)
                    if category_id else None)
        author = Profile.objects.get(user=request.user)
        article = Article.objects.create(
            title=title,
            category=category,
            entry=entry,
            header_image=header_image,
            author=author
        )
        return redirect('blog:article_detail', id=article.id)

    categories = ArticleCategory.objects.all()
    return render(request, 'article_detail.html', {
        'categories': categories,
        'is_editing': True,
    })


@login_required
def article_update(request, id):
    """Update an existing article."""
    article = get_object_or_404(Article, id=id)

    if article.author != request.user.profile:
        return redirect('blog:index')

    if request.method == 'POST':
        if 'delete' in request.POST:
            article.delete()
            return redirect('blog:index')
        article.title = request.POST.get('title')
        category_id = request.POST.get('category')
        article.entry = request.POST.get('entry')
        article.header_image = request.FILES.get(
            'header_image', article.header_image
            )
        article.category = (ArticleCategory.objects.get(id=category_id)
                            if category_id else None)
        article.save()
        return redirect('blog:article_detail', id=article.id)

    categories = ArticleCategory.objects.all()
    return render(request, 'article_detail.html', {
        'article': article,
        'categories': categories,
        'is_editing': True,
    })
