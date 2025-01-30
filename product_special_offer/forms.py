# product_special_offer/forms.py
from django import forms
from .models import SpecialOffer


class SpecialOfferForm(forms.ModelForm):
    class Meta:
        model = SpecialOffer
        fields = ['product', 'discount_percentage', 'offer_start_date', 'offer_end_date', 'image']
