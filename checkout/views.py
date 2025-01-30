from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from product.models import Cart


@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:sammury')  # Redirecting to the payment view in the product app
    else:
        form = CheckoutForm()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'checkout/checkout.html', {'form': form, 'item_count': item_count})
