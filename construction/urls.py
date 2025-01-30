from django.urls import path
from . import views

urlpatterns = [
    path('', views.construction, name='construction'),
    path('residential/', views.residential, name='residential'),
    path('commercial/', views.commercial, name='commercial'),
    path('civil_engineering/', views.civil_engineering, name='civil_engineering'),
    path('specialized/', views.specialized, name='specialized'),
]
