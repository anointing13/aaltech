from django.shortcuts import render
from .models import FAQ
from .forms import FAQSearchForm
from product.models import Cart


def faq_list(request):
    form = FAQSearchForm(request.POST or None)  # Use POST instead of GET
    search_query = request.POST.get('search_query')

    if search_query:
        # If a search query exists, search in both visible and hidden FAQs
        faqs = FAQ.objects.filter(question__icontains=search_query)  # Matching FAQs
    else:
        # Otherwise, show only the visible FAQs
        faqs = FAQ.objects.filter(hidden=False)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'faq/faq_list.html', {'faqs': faqs, 'form': form, 'item_count': item_count})
