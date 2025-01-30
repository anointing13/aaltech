from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AppointmentForm, OrderForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Order  # Ensure this import is correct
from django.contrib.auth.decorators import user_passes_test
from .forms import FuelPriceForm
from .models import FuelPrice, FuelPriceHistory
from django.utils.dateformat import DateFormat
from .utils import get_fuel_price
from django.http import JsonResponse

import logging


@login_required
def oilgas(request):
    # Fetch the current price instance using the utility function
    fuel_price = get_fuel_price()

    # Fetch price history for the chart
    history = FuelPriceHistory.objects.all().order_by('timestamp')

    # Print the records for debugging
    for record in history:
        print(record.timestamp, record.super_price, record.lpg_price)

    price_history_dates = [DateFormat(h.timestamp).format('Y-m-d') for h in history]
    super_price_history = [float(h.super_price) for h in history]  # Convert Decimal to float
    lpg_price_history = [float(h.lpg_price) for h in history]

    # Debugging prints
    print(price_history_dates)  # Check if dates are populated correctly
    print(super_price_history)  # Check if super prices are populated correctly
    print(lpg_price_history)  # Check if LPG prices are populated correctly

    # Pass the data to the template
    return render(request, 'oilgas/oilgas.html', {
        'fuel_price': fuel_price,
        'price_history_dates': price_history_dates,
        'super_price_history': super_price_history,
        'lpg_price_history': lpg_price_history,
    })


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user  # Associate with the logged-in user
            appointment.save()

            # Retrieve the customer's full name
            customer_name = f"{request.user.first_name} {request.user.last_name}".strip()  # Concatenate first and last name

            # Compose a modern email message
            email_subject = 'Your Appointment at ANTE OMNIA Has Been Confirmed'
            email_body = (
                f"Dear {customer_name},\n\n"
                "Thank you for scheduling your appointment with ANTE OMNIA. We're pleased to confirm your booking.\n\n"
                "Details:\n"
                " Location: [Insert Location or Online Link]\n\n"
                "Please note, if there’s any conflict with your requested date or time, we’ll contact you to suggest an alternative. "
                "We truly appreciate your patience and understanding.\n\n"
                "If you have any questions or need to modify your appointment, feel free to reach out to us at support@anteomnia.com or visit our website: https://www.anteomnia.com.\n\n"
                "Best regards,\n"
                "The ANTE OMNIA Team\n"
                "Website: https://www.anteomnia.com\n"
                "Phone: +233 5577 70955 / 2494 87009"
            )

            # Send the email
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],  # Send email to the logged-in user's email
                fail_silently=False,
            )

            # Pass the customer's name to the success template
            return render(request, 'oilgas/appointment_success.html', {'customer_name': customer_name})
    else:
        form = AppointmentForm()

    return render(request, 'oilgas/book_appointment.html', {'form': form})


@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user  # Associate with the logged-in user
            order.save()

            # Fetch the additional order details from the database
            tonnage = order.tonnage  # Assuming this is a field in the Order model
            super_lpg = order.super_lpg  # Assuming this is a field in the Order model
            quantity_of_load = order.quantity_of_load  # Assuming this is a field in the Order model
            tank_capacity = order.tank_capacity  # Assuming this is a field in the Order model

            # Send email notification
            customer_email = request.user.email  # Get the user's email
            customer_name = f"{request.user.first_name} {request.user.last_name}".strip()  # Concatenate first and last name

            # Compose the modern email message with additional order details
            email_subject = 'Your Order with ANTE OMNIA Has Been Successfully Placed'
            email_body = (
                f"Dear {customer_name},\n\n"
                "Thank you for placing your order with ANTE OMNIA. We’re pleased to confirm that your order has been successfully processed.\n\n"
                "Order Details:\n"
                f" Tonnage: {tonnage} tons\n"
                f" Super LPG: {super_lpg}\n"
                f" Quantity of Load: {quantity_of_load} units\n"
                f" Tank Capacity: {tank_capacity} liters\n\n"
                # "Your order is being prepared, and we’ll notify you once it’s ready for delivery.\n\n"
                "If you have any questions or need to make changes to your order, please reach out to us at support@anteomnia.com or visit our website: https://www.anteomnia.com.\n\n"
                "Best regards,\n"
                "The ANTE OMNIA Team\n"
                "Website: https://www.anteomnia.com\n"
                "Phone: +233 5577 70955 / 2494 87009"
            )

            # Send the email
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                fail_silently=False,
            )

            # Pass the customer's name to the success template
            return render(request, 'oilgas/order_success.html', {'customer_name': customer_name})
    else:
        form = OrderForm()

    return render(request, 'oilgas/place_order.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)  # Only allow staff users (admins) to update the prices
def update_fuel_price(request):
    # Fetch the current price instance or create a new one if none exists
    fuel_price, created = FuelPrice.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = FuelPriceForm(request.POST, instance=fuel_price)
        if form.is_valid():
            form.save()
            return redirect('update_fuel_price')  # Redirect to the same page after successful update
    else:
        form = FuelPriceForm(instance=fuel_price)

    # Render the fuel prices and form for updating
    return render(request, 'oilgas/oilgas.html', {'form': form, 'fuel_price': fuel_price})
