# points_wallet/urls.py
from django.urls import path
from . import views

app_name = 'points_wallet'  # This is crucial for using the namespace 'points_wallet'

urlpatterns = [
    path('wallet/', views.wallet_view, name='wallet_view'),
    path('withdraw/', views.withdraw_view, name='withdraw_view'),
    path('purchase/<int:product_id>/', views.purchase_view, name='purchase_view'),
    path('withdrawal-history/', views.withdrawal_history, name='withdrawal_history'),
]
