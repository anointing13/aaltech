from django.urls import path
from . import views

urlpatterns = [
    path('financial_reports/', views.financial_reports_list, name='financial_reports'),  # Reports list page
    path('financial_report/<slug:slug>/', views.financial_reports_detail, name='financial_report_detail'),  # Report detail page
]

