from django import forms


class FAQSearchForm(forms.Form):
    search_query = forms.CharField(label='Search FAQs', max_length=100, required=False)
