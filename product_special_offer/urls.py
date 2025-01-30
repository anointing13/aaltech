# product_special_offer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_special_offer, name='add_special_offer'),
    path('list/', views.special_offer_list, name='special_offer_list'),
]
