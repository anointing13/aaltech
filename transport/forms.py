from django import forms
from .models import Booking, Review


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'from_destination', 'to_destination', 'booking_date', 'price_to_pay']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define the regions and cities (grouped choices)
        REGION_CITY_CHOICES = [
            ('Greater Accra Region', [
                ('Accra', 'Accra'),
                ('Tema', 'Tema'),
                ('Madina', 'Madina'),
                ('Teshie', 'Teshie'),
                ('Nungua', 'Nungua'),
            ]),
            ('Ashanti Region', [
                ('Kumasi', 'Kumasi'),
                ('Obuasi', 'Obuasi'),
                ('Ejisu', 'Ejisu'),
                ('Mampong', 'Mampong'),
                ('Konongo', 'Konongo'),
            ]),
            ('Western Region', [
                ('Sekondi-Takoradi', 'Sekondi-Takoradi'),
                ('Tarkwa', 'Tarkwa'),
                ('Axim', 'Axim'),
                ('Prestea', 'Prestea'),
                ('Sefwi-Wiawso', 'Sefwi-Wiawso'),
            ]),
            ('Eastern Region', [
                ('Koforidua', 'Koforidua'),
                ('Akim Oda', 'Akim Oda'),
                ('Nkawkaw', 'Nkawkaw'),
                ('Suhum', 'Suhum'),
                ('Akwatia', 'Akwatia'),
            ]),
            ('Volta Region', [
                ('Ho', 'Ho'),
                ('Keta', 'Keta'),
                ('Hohoe', 'Hohoe'),
                ('Aflao', 'Aflao'),
                ('Denu', 'Denu'),
            ]),
            ('Northern Region', [
                ('Tamale', 'Tamale'),
                ('Yendi', 'Yendi'),
                ('Savelugu', 'Savelugu'),
                ('Bimbilla', 'Bimbilla'),
                ('Salaga', 'Salaga'),
            ]),
            ('Central Region', [
                ('Cape Coast', 'Cape Coast'),
                ('Elmina', 'Elmina'),
                ('Winneba', 'Winneba'),
                ('Mankessim', 'Mankessim'),
                ('Saltpond', 'Saltpond'),
            ]),
            ('Upper East Region', [
                ('Bolgatanga', 'Bolgatanga'),
                ('Navrongo', 'Navrongo'),
                ('Bawku', 'Bawku'),
                ('Zebilla', 'Zebilla'),
                ('Sandema', 'Sandema'),
            ]),
            ('Upper West Region', [
                ('Wa', 'Wa'),
                ('Lawra', 'Lawra'),
                ('Tumu', 'Tumu'),
                ('Nandom', 'Nandom'),
                ('Jirapa', 'Jirapa'),
            ]),
            ('Bono Region', [
                ('Sunyani', 'Sunyani'),
                ('Berekum', 'Berekum'),
                ('Dormaa Ahenkro', 'Dormaa Ahenkro'),
                ('Wenchi', 'Wenchi'),
                ('Bechem', 'Bechem'),
            ]),
            ('Bono East Region', [
                ('Techiman', 'Techiman'),
                ('Kintampo', 'Kintampo'),
                ('Nkoranza', 'Nkoranza'),
                ('Atebubu', 'Atebubu'),
                ('Yeji', 'Yeji'),
            ]),
            ('Western North Region', [
                ('Sefwi-Wiawso', 'Sefwi-Wiawso'),
                ('Bibiani', 'Bibiani'),
                ('Enchi', 'Enchi'),
                ('Juaboso', 'Juaboso'),
                ('Akontombra', 'Akontombra'),
            ]),
            ('Oti Region', [
                ('Dambai', 'Dambai'),
                ('Nkwanta', 'Nkwanta'),
                ('Kete Krachi', 'Kete Krachi'),
                ('Jasikan', 'Jasikan'),
                ('Chinderi', 'Chinderi'),
            ]),
            ('Ahafo Region', [
                ('Goaso', 'Goaso'),
                ('Bechem', 'Bechem'),
                ('Kenyasi', 'Kenyasi'),
                ('Duayaw Nkwanta', 'Duayaw Nkwanta'),
                ('Hwidiem', 'Hwidiem'),
            ]),
            ('Savannah Region', [
                ('Damongo', 'Damongo'),
                ('Bole', 'Bole'),
                ('Salaga', 'Salaga'),
                ('Daboya', 'Daboya'),
                ('Sawla', 'Sawla'),
            ]),
            ('North East Region', [
                ('Nalerigu', 'Nalerigu'),
                ('Walewale', 'Walewale'),
                ('Gambaga', 'Gambaga'),
                ('Bunkpurugu', 'Bunkpurugu'),
                ('Chereponi', 'Chereponi'),
            ]),
        ]

        # Assign the grouped city choices to the dropdowns
        self.fields['from_destination'] = forms.ChoiceField(choices=REGION_CITY_CHOICES)
        self.fields['to_destination'] = forms.ChoiceField(choices=REGION_CITY_CHOICES)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
