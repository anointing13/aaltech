from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Review, LoyaltyPoints
from .forms import BookingForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
import requests


@login_required
def transport(request):
    return render(request, 'transport/transport.html')


@login_required
def success_view(request):
    return render(request, 'transport/success.html')


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'transport/booking_history.html', {'bookings': bookings})


@login_required
def recommended_bookings(request):
    # For example, showing the latest 5 bookings (you can customize the logic)
    recommended_bookings = Booking.objects.all()[:5]
    return render(request, 'transport/recommended_bookings.html', {'bookings': recommended_bookings})


@login_required
def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Process the booking
            booking_instance = form.save()

            # Prepare email content for admin
            subject = 'New Booking Received'
            message = f"""
            A new booking has been made.

            Booking Details:
            From: {booking_instance.from_destination}
            To: {booking_instance.to_destination}
            Price: GHS {booking_instance.price_to_pay} 
            User: {request.user.email}
            """
            # Send email to admins
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['admin@example.com'],  # Add admin email here
                fail_silently=False,
            )

            # Prepare email content for user confirmation
            user_subject = 'Your Booking Confirmation From  Ante Omnia Transport Service'
            user_message = f"""
            Dear {request.user.first_name}, 

            Thank you for your booking! Here are your booking details:

            From: {booking_instance.from_destination}
            To: {booking_instance.to_destination}
            Price: GHS {booking_instance.price_to_pay:.2f}

            We look forward to serving you!

            Best regards,
            Your Booking Team
            """
            # Send email to the user
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],  # Send confirmation to the user
                fail_silently=False,
            )

            # Redirect to the success page
            return redirect('transport:success')  # Use the named URL for the success page
    else:
        form = BookingForm()

    return render(request, 'transport/make_booking.html', {'form': form})


# Example of static pricing based on destination pairs
PRICES = {
    # Existing routes
    ('Accra', 'Kumasi'): 120.00,
    ('Kumasi', 'Accra'): 120.00,
    ('Accra', 'Tamale'): 110.00,
    ('Tamale', 'Accra'): 110.00,
    ('Accra', 'Cape Coast'): 33.00,
    ('Cape Coast', 'Accra'): 33.00,
    ('Accra', 'Wa'): 105.00,
    ('Wa', 'Accra'): 105.00,
    ('Accra', 'Bolgatanga'): 125.00,
    ('Bolgatanga', 'Accra'): 125.00,
    ('Accra', 'Sunyani'): 50.00,
    ('Sunyani', 'Accra'): 50.00,
    ('Accra', 'Takoradi'): 55.00,
    ('Takoradi', 'Accra'): 55.00,
    ('Accra', 'Ho'): 29.00,
    ('Ho', 'Accra'): 29.00,
    ('Kumasi', 'Tamale'): 60.00,
    ('Tamale', 'Kumasi'): 60.00,
    ('Kumasi', 'Bolgatanga'): 70.00,
    ('Bolgatanga', 'Kumasi'): 70.00,
    ('Kumasi', 'Wa'): 65.00,
    ('Wa', 'Kumasi'): 65.00,
    ('Kumasi', 'Takoradi'): 30.00,
    ('Takoradi', 'Kumasi'): 30.00,
    ('Cape Coast', 'Takoradi'): 20.00,
    ('Takoradi', 'Cape Coast'): 20.00,
    ('Takoradi', 'Tamale'): 100.00,
    ('Tamale', 'Takoradi'): 100.00,
    ('Takoradi', 'Bolgatanga'): 110.00,
    ('Bolgatanga', 'Takoradi'): 110.00,
    ('Tamale', 'Wa'): 40.00,
    ('Wa', 'Tamale'): 40.00,

    # Additional routes for expanded coverage
    ('Cape Coast', 'Sunyani'): 45.00,
    ('Sunyani', 'Cape Coast'): 45.00,
    ('Wa', 'Bolgatanga'): 90.00,
    ('Bolgatanga', 'Wa'): 90.00,
    ('Ho', 'Takoradi'): 65.00,
    ('Takoradi', 'Ho'): 65.00,
    ('Kumasi', 'Ho'): 80.00,
    ('Ho', 'Kumasi'): 80.00,
    ('Tamale', 'Ho'): 75.00,
    ('Ho', 'Tamale'): 75.00,
    ('Cape Coast', 'Tamale'): 150.00,
    ('Tamale', 'Cape Coast'): 150.00,
    ('Accra', 'Ho'): 60.00,
    ('Ho', 'Accra'): 60.00,
    ('Kumasi', 'Sunyani'): 40.00,
    ('Sunyani', 'Kumasi'): 40.00,
    ('Wa', 'Sunyani'): 55.00,
    ('Sunyani', 'Wa'): 55.00,
    ('Takoradi', 'Wa'): 80.00,
    ('Wa', 'Takoradi'): 80.00,
    ('Bolgatanga', 'Ho'): 95.00,
    ('Ho', 'Bolgatanga'): 95.00,
    ('Cape Coast', 'Wa'): 120.00,
    ('Wa', 'Cape Coast'): 120.00,
    # Add any additional inter-regional routes if needed
}


@login_required
def get_transport_price(request):
    from_destination = request.GET.get('from_destination')
    to_destination = request.GET.get('to_destination')

    if from_destination and to_destination:
        # Get the price from the static dictionary
        price = PRICES.get((from_destination, to_destination), 'N/A')
        return JsonResponse({'price': str(price)})

    return JsonResponse({'price': 'N/A'})


@login_required
def user_profile(request):
    loyalty_points = LoyaltyPoints.objects.get(user=request.user)
    return render(request, 'transport/profile.html', {'loyalty_points': loyalty_points})


@login_required
def comfort(request):
    return render(request, 'transport/comfort_convenience.html')


@login_required
def safety(request):
    return render(request, 'transport/safety_tracking.html')


@login_required
def accessibility(request):
    return render(request, 'transport/booking_accessibility.html')


@login_required
def interstate(request):
    return render(request, 'transport/interstate_route_services.html')

