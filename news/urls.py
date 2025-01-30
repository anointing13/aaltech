from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),  # URL for the news list
    path('<slug:slug>/', views.news_detail, name='news_detail'),  # URL for individual news detail using slug
]
