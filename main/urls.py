from django.urls import path
from . import views
# accès aux différents fichiers
urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('change_language/<str:language>/', views.change_language, name='change_language'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('index_articles/', views.index_articles, name='index_articles'),
    path('search_articles/', views.search_articles, name='search_articles'),
]
