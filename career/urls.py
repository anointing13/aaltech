from django.urls import path
from . import views

urlpatterns = [
    path('career/', views.career_view, name='career_form'),
    path('career/success/', views.career_success, name='career_success'),  # Success URL
]
