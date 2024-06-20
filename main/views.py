from django.shortcuts import render, redirect
from .models import Article
from django.utils import translation 
from django.conf import settings

def article_list(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'main/article_list.html', context)

def change_language(request, language):
    translation.activate(language)
    response = redirect('/')
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
