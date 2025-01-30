# recent_product/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('recent-products/', views.recent_products_view, name='recent_products'),
]
