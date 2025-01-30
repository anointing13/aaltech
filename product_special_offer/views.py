# product_special_offer/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import SpecialOffer
from .forms import SpecialOfferForm


def add_special_offer(request):
    if request.method == 'POST':
        form = SpecialOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('special_offer_list')
    else:
        form = SpecialOfferForm()
    return render(request, 'product_special_offer/add_special_offer.html', {'form': form})


def special_offer_list(request):
    active_offers = SpecialOffer.objects.filter(offer_end_date__gte=timezone.now())
    return render(request, 'product_special_offer/special_offer_list.html', {'active_offers': active_offers})
