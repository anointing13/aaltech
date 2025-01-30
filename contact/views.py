from django.shortcuts import render

from .forms import ContactForm
from .models import Contact
from product.models import Cart


# Create your views here.

def contact(request):
    message = ""
    product = Contact.objects.all()
    forms = ContactForm

    if request.method == "POST":
        forms = ContactForm(request.POST)
        if forms.is_valid():
            forms.save()
            request.POST = ""
            message = "Message Sent Successfully"
        else:
            message = "Message Not Sent"

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = cart.items.count()  # Get the cart item count
    else:
        item_count = 0  # No items in the cart for anonymous users

    return render(request, 'contact/contact.html', {'key': product, 'form': forms, 'message': message, 'item_count': item_count})