from django.shortcuts import render
from .models import HiddenProduct


def search_hidden_products(request):
    query = request.POST.get('query', '').strip()
    hidden_products = HiddenProduct.get_hidden_products(query=query)

    return render(request, 'hidden_product/search_results.html', {'hidden_products': hidden_products, 'query': query})
