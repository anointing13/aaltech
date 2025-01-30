# recent_product/views.py
from django.shortcuts import render
from .models import RecentProduct


def recent_products_view(request):
    # Fetch all recent products with related product details
    recent_products = RecentProduct.objects.select_related('product').order_by('-date_added')

    context = {
        'recent_products': recent_products
    }
    # Render 'index.html' in the main 'product' app
    return render(request, 'product/index.html', context)
