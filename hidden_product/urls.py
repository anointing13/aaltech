from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_hidden_products, name='search_hidden_products'),
]
