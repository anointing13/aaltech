# news/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('investor_relations/', views.investor_relations_news, name='investor_relations'),
    path('investor-relations/news/<slug:slug>/', views.news_detail, name='news_detail'),
]

