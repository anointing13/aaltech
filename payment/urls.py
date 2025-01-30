from django.urls import path
from . import views

app_name = 'payment'  # This defines the namespace for the payment app

urlpatterns = [
    path('payment/', views.payment_view, name='payment_view'),
    path('', views.payment_view, name='payment_view'),  # Payment view
    path('process/', views.process_payment, name='process_payment'),  # Process payment
    path('mobile_money/<int:order_id>/', views.mobile_money_payment, name='mobile_money_payment'),
    # Mobile money payment
    path('credit_card/<int:order_id>/', views.credit_card_payment, name='credit_card_payment'),  # Credit card payment
    path('bank_transfer/<int:order_id>/', views.bank_transfer_payment, name='bank_transfer_payment'),
    # Bank transfer payment
    path('orders/', views.user_orders, name='user_orders'),
    path('callback/', views.payment_callback, name='callback'),
]





