from django.shortcuts import render
from django.utils import timezone

from .models import Product
from django.db.models import Q
from .forms import ProductFilterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from decimal import Decimal
from .models import Favorite
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from product_special_offer.models import SpecialOffer
from recent_product.models import RecentProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from newsletter.models import Subscriber
from django.utils.timezone import now


def show(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'product/detail.html', {'key': product, 'item_count': item_count})


def home(request):
    # Fetch all main products, excluding hidden products
    products = Product.objects.filter(is_hidden=False)  # Only show non-hidden products

    # Get active special offers
    active_offers = SpecialOffer.objects.filter(
        offer_start_date__lte=timezone.now(),
        offer_end_date__gte=timezone.now()
    )

    # Set up pagination for main products
    paginator = Paginator(products, 3)  # Show 3 products per page
    page_number = request.GET.get('page')

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    # Get cart item count
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    # Fetch recent products for the homepage and apply pagination
    recent_products = RecentProduct.objects.select_related('product').order_by('-date_added')

    # Set up pagination for recent products (show 6 recent products per page)
    recent_paginator = Paginator(recent_products, 4)  # Show 4 recent products per page
    recent_page_number = request.GET.get('recent_page')

    try:
        paginated_recent_products = recent_paginator.page(recent_page_number)
    except PageNotAnInteger:
        paginated_recent_products = recent_paginator.page(1)
    except EmptyPage:
        paginated_recent_products = recent_paginator.page(recent_paginator.num_pages)

    return render(request, 'product/index.html', {
        'key': paginated_products,  # Paginated main products
        'item_count': item_count,  # Cart item count
        'active_offers': active_offers,  # Active offers
        'recent_products': paginated_recent_products,  # Standalone paginated recent products
    })


def about(request):
    product = Product.objects.all()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'product/about.html', {'key': product, 'item_count': item_count})


def shop(request):
    # Fetch all products that are not hidden
    product_list = Product.objects.filter(is_hidden=False)

    # Implement search functionality
    if request.method == "POST":
        if request.POST.get('search'):
            search_query = request.POST['search']
            product_list = product_list.filter(Q(name__icontains=search_query))

    # Pagination
    paginator = Paginator(product_list, 3)  # Show 3 products per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided

    # Ensure the page number is an integer
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1  # Default to page 1 if the conversion fails

    # Pagination logic
    try:
        products = paginator.page(page_number)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        products = paginator.page(paginator.num_pages)

    # Debugging output
    print(f"Requested page number: {page_number}")
    print(f"Total number of products: {paginator.count}")
    print(f"Total number of pages: {paginator.num_pages}")

    # Cart item count logic
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'product/shop.html', {
        'key': products,  # Paginated products
        'item_count': item_count  # Cart item count
    })


def filter_view(request):
    form = ProductFilterForm(request.POST or None)

    # Start by filtering only visible products by default
    products = Product.objects.filter(is_hidden=False)
    item_count = 0  # Initialize item_count

    if request.method == 'POST' and form.is_valid():
        selected_prices = request.POST.getlist('price')

        if selected_prices:
            # Apply price filtering to the products
            products = filter_by_price(products, selected_prices)

        # After filtering by price, include hidden products if `show_hidden` is true
        show_hidden = request.POST.get('show_hidden', 'false') == 'true'
        if show_hidden:
            products = products | Product.objects.filter(is_hidden=True)

        # Get cart item count if user is authenticated
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            item_count = cart.items.count()
        else:
            item_count = 0

    # Pagination
    paginator = Paginator(products, 3)  # 3 products per page
    page_number = request.GET.get('page')
    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    return render(request, 'product/shop.html', {
        'key': paginated_products,  # Pass paginated products
        'form': form,
        'item_count': item_count
    })


def filter_by_price(queryset, selected_prices):
    for price_range in selected_prices:
        if price_range == 'all':
            continue
        min_price, max_price = map(int, price_range.split('-'))
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
    return queryset


# Define the shipping fee as a constant (ensure it's a Decimal type)
SHIPPING_FEE = Decimal('200.00')  # Ensure shipping fee is a Decimal


@login_required
def cart_view(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get all the items in the cart
    items = cart.items.all()

    # Calculate subtotal: sum of item total prices (which now include discounts)
    subtotal = sum(item.get_total_price() for item in items)

    # Calculate total price (subtotal + shipping fee)
    total_price = subtotal + SHIPPING_FEE

    # Get the cart item count
    item_count = cart.items.count()

    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'shipping_fee': SHIPPING_FEE,
        'total_price': total_price,
        'item_count': item_count,
    }
    return render(request, 'product/cart.html', context)


# View to add a product to the cart
# views.py for handling the cart logic

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the cart item already exists, increase the quantity
        cart_item.quantity += 1
    else:
        # Set the initial quantity to 1 for a new cart item
        cart_item.quantity = 1

    cart_item.save()

    # Recalculate the total price of the cart after saving the item
    cart.total_price = sum(item.get_total_price() for item in cart.items.all())
    cart.save()

    return redirect('cart')  # Redirect to the cart page after adding


# View to update cart item quantity
@login_required
def cart_update_quantity(request, item_id, action):
    # Get the cart item for the current user
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # Update the quantity of the cart item
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Update the total price of the cart
    cart.total_price = sum(item.get_total_price() for item in cart.items.all())
    cart.save()

    return redirect('cart')  # Redirect back to the cart page


# View to remove an item from the cart
@login_required
def cart_remove_item(request, item_id):
    # Get the cart item for the current user
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # Get or create the cart for the current user
    cart = cart_item.cart

    # Remove the item from the cart
    cart_item.delete()

    # Update the total price of the cart
    cart.total_price = sum(item.get_total_price() for item in cart.items.all())
    cart.save()

    return redirect('cart')  # Redirect back to the cart page


# View to add a product to the favorites


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If the product is already in favorites, you can choose to handle this (e.g., show a message)
        pass

    # Determine where to redirect based on the referring URL
    referer = request.META.get('HTTP_REFERER', '/')

    if 'index' in referer:
        return redirect('home')  # Adjust if your index page URL name is different
    elif 'shop' in referer:
        return redirect('shop')  # Adjust if your shop page URL name is different

    # Default fallback
    return redirect('shop')


# View to display the favorites page
@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'product/favorites.html', {'favorites': favorites, 'item_count': item_count})


# View to remove a product from favorites
@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = get_object_or_404(Favorite, user=request.user, product=product)
    favorite.delete()
    return redirect('favorites_list')


# View to list all favorite products
@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'product/favorites.html', {'favorites': favorites})


@login_required
def favorite_count(request):
    count = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})


@login_required
def payment_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    if cart:
        items = cart.items.all()  # Get all items related to this cart
    else:
        items = []

    item_count = items.count()
    total_price = sum(item.get_total_price() for item in items)
    shipping_fee = 200.00  # Adjust this as needed

    context = {
        'items': items,
        'item_count': item_count,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
    }
    return render(request, 'product/summary.html', context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=400)

        # Check if the email is already subscribed
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'error': 'This email is already subscribed.'}, status=400)

        # Save the new subscriber
        Subscriber.objects.create(email=email, subscribed_at=now())
        return JsonResponse({'message': 'Subscription successful!'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def products_data(request):
    products = list(Product.objects.values('id', 'name', 'price', 'category__name', 'brand__name', 'image'))
    return JsonResponse(products, safe=False)