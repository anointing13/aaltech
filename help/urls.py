from django.urls import path
from . import views

urlpatterns = [
    # Other URLs for your app
    path('help/', views.help_page, name='help'),
]
