from django.urls import path
from .views import booking_history, recommended_bookings, make_booking, user_profile, success_view
from . import views

app_name = 'transport'  # Add this line to define the app namespace

urlpatterns = [
    path('transport/', views.transport, name='transport'),
    path('booking_history/', booking_history, name='booking_history'),
    path('recommended_bookings/', recommended_bookings, name='recommended_bookings'),
    path('transport/make_booking/', make_booking, name='make_booking'),
    path('profile/', user_profile, name='profile'),
    path('make_booking/', make_booking, name='make_booking'),  # This defines the pattern
    path('get_transport_price/', views.get_transport_price, name='get_transport_price'),
    path('success/', success_view, name='success'),  # Ensure you have a success view
    path('comfort/', views.comfort, name='comfort'),
    path('accessibility/', views.accessibility, name='accessibility'),
    path('safety/', views.safety, name='safety'),
    path('interstate/', views.interstate, name='interstate'),

]
