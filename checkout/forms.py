from django import forms
from .models import CheckoutDetail

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutDetail
        fields = [
            'first_name', 'last_name', 'email', 'mobile_no', 'address_line_1', 'address_line_2', 'country', 'city',
            'state', 'zip_code', 'create_account', 'ship_to_different_address',
            'shipping_first_name', 'shipping_last_name', 'shipping_email', 'shipping_mobile_no', 'shipping_address_line_1',
            'shipping_address_line_2', 'shipping_country', 'shipping_city', 'shipping_state', 'shipping_zip_code'
        ]
