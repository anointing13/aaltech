from django.urls import path
from . import views

urlpatterns = [
    path('press_release/', views.press_release_list, name='financial_reports'),  # Reports list page
    path('press_release/<slug:slug>/', views.press_release_detail, name='news_detail'),  # Report detail page
]
