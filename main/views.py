from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'main/article_list.html', context)

