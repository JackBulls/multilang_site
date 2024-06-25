import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from .models import Article
from django.utils import translation 
from django.conf import settings
from .elasticsearch_helper import create_index, index_document, search_document

openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def chatbot(request):
    
    # Gère les requêtes du chatbot. Accepte une requête POST contenant un message utilisateur,
    # génère une réponse à l'aide de l'API GPT-3 et renvoie la réponse.
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '')

        # Appel à l'API GPT-3 pour générer une réponse
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=user_input,
            max_tokens=150
        )

        message = response.choices[0].text.strip()
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Invalid request'}, status=400)

def article_list(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    # accès à la page article
    return render(request, 'main/article_list.html', context)

def change_language(request, language):
    translation.activate(language)
    response = redirect('/')
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response

def index_articles(request):
    create_index('articles')
    articles = Article.objects.all()
    for article in articles:
        document = {
            'title': article.title,
            'content': article.content,
            'publication_date': article.publication_date
        }
        index_document('articles', 'article', document)
    return JsonResponse({'message': 'Articles indexed successfully'})

def search_articles(request):
    
    # Gère les requêtes de recherche. Accepte une requête GET avec une query,
    # recherche les articles correspondants dans Elasticsearch et renvoie les résultats augmentés par IA.
    query = request.GET.get('query', '')
    search_query = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title', 'content']
            }
        }
    }
    results = search_document('articles', search_query)
    # Augmente les résultats de la recherche avec GPT-3
    augmented_results = []
    for result in results['hits']['hits']:
        augmented_content = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Summarize this article: {result['_source']['content']}",
            max_tokens=150
        ).choices[0].text.strip()

        augmented_results.append({
            'title': result['_source']['title'],
            'content': result['_source']['content'],
            'augmented_content': augmented_content,
            'publication_date': result['_source']['publication_date']
        })

    return JsonResponse(augmented_results, safe=False)

def home(request):
    # Accès à la page d'accueil
    return render(request, 'main/home.html')