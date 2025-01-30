from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from product.models import Cart  # Import the Cart model from your product app
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
import requests
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def payment_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        items = []

    item_count = items.count()
    total_price = sum(item.get_total_price() for item in items)  # Assuming get_total_price returns a Decimal
    shipping_fee = Decimal('200.00')  # Convert shipping fee to Decimal
    total_with_shipping = total_price + shipping_fee  # Now both are Decimal types

    context = {
        'items': items,
        'item_count': item_count,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'total_with_shipping': total_with_shipping,
    }
    return render(request, 'payment/payment.html', context)


@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')  # Get selected payment method
        total_amount = request.POST.get('total_amount')  # Get total amount from form

        # Retrieve user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return redirect('payment:payment_view')  # Handle case where cart does not exist

        # Calculate shipping fee
        shipping_fee = calculate_shipping_fee(cart)

        # Convert total_amount to Decimal and add shipping fee
        try:
            total_amount = Decimal(total_amount) + shipping_fee
        except (InvalidOperation, ValueError):
            return redirect('payment:payment_view')  # Handle invalid amount

        # Create the Order
        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            total_amount=total_amount
        )

        # Save each item in the cart to OrderItem
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.get_total_price()
            )

        # Clear the cart after order creation
        cart.items.all().delete()

        # Redirect based on payment method
        if payment_method == 'mobilemoney':
            return redirect('payment:mobile_money_payment', order_id=order.id)
        elif payment_method == 'creditcard':
            return initialize_credit_card_payment(order)
        elif payment_method == 'banktransfer':
            return redirect('payment:bank_transfer_payment', order_id=order.id)

    return redirect('payment:payment_view')  # Redirect back to the payment view if not a POST request


def calculate_shipping_fee(cart):
    # Example logic: fixed fee or based on the number of items
    return Decimal('200.00') if cart.items.count() > 0 else Decimal('0.00')


def initialize_credit_card_payment(order):
    # Logic to initialize credit card payment using Paystack
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',  # Replace with your Paystack secret key
        'Content-Type': 'application/json'
    }

    data = {
        'email': order.user.email,
        'amount': int(order.total_amount * 100),  # Amount in kobo
        'order_id': order.id,  # Your order ID
        'currency': 'GHS',  # Change this to your desired currency
        'callback_url': 'http://yourwebsite.com/payment/callback/'  # Update this URL
    }

    response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
    response_data = response.json()

    if response_data['status']:
        payment_url = response_data['data']['authorization_url']
        return redirect(payment_url)  # Redirect to Paystack payment page
    else:
        return redirect('payment:payment_view')  # Handle initialization failure


@login_required
def mobile_money_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'payment/mobile_money_payment.html', {'order': order})
    except Order.DoesNotExist:
        return redirect('payment:payment_view')  # Redirect if the order does not exist


@login_required
def credit_card_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'payment/credit_card_payment.html', {'order': order})
    except Order.DoesNotExist:
        return redirect('payment:payment_view')  # Redirect if the order does not exist


@login_required
def bank_transfer_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'payment/bank_transfer_payment.html', {'order': order})
    except Order.DoesNotExist:
        return redirect('payment:payment_view')  # Redirect if the order does not exist



def payment_callback(request):
    # This view should handle payment confirmations or webhook callbacks
    if request.method == 'POST':
        # Process the payment confirmation or handle the callback
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def user_orders(request):
    # Retrieve all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    # For each order, get the related order items
    order_items = OrderItem.objects.filter(order__in=orders)

    context = {
        'orders': orders,
        'order_items': order_items
    }

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'payment/user_orders.html', {**context, 'item_count': item_count})
