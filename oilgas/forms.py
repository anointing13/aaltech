from django import forms
from .models import Appointment, Order
from .models import FuelPrice


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'message']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = True
        self.fields['message'].required = True


class OrderForm(forms.ModelForm):
    # Set custom label for super_lpg field
    super_lpg = forms.ChoiceField(label="Super / LPG", choices=Order.SUPER_LPG_CHOICES)

    class Meta:
        model = Order
        fields = ['tonnage', 'super_lpg', 'quantity_of_load', 'tank_capacity', 'station_name', 'car_number',
                  'driver_name']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Disable 'LPG' and 'Petrol and Diesel' options by adding the 'disabled' attribute
        self.fields['tonnage'].choices = [
            (value, label) if value not in ['LPG', 'petrol-diesel'] else (value, label + ' (Not Selectable)')
            for value, label in self.fields['tonnage'].choices
        ]
        self.fields['tonnage'].widget.attrs['onchange'] = """
            if (this.value === 'LPG' || this.value === 'petrol-diesel') {
                alert('LPG and Petrol/Diesel are not selectable. Please choose another option.');
                this.value = '';  // Reset the value to prevent selection
            }
        """


class FuelPriceForm(forms.ModelForm):
    class Meta:
        model = FuelPrice
        fields = ['super_price_per_liter', 'lpg_price_per_kilo']
        widgets = {
            'super_price_per_liter': forms.TextInput(attrs={'class': 'form-control'}),
            'lpg_price_per_kilo': forms.TextInput(attrs={'class': 'form-control'}),
        }
