from django.urls import path
from . import views
from .views import update_fuel_price

urlpatterns = [
    path('admin/oilgas/', views.oilgas, name='oilgas'),  # Registering the oilgas view
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('place-order/', views.place_order, name='place_order'),
    path('', views.oilgas, name='oilgas'),
    path('update-fuel-price/', update_fuel_price, name='update_fuel_price'),
]
