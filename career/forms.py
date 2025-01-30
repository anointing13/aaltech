from django import forms
from .models import Career

class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['name', 'email', 'phone_number', 'address', 'cv', 'cover_letter']
        widgets = {
            'cv': forms.ClearableFileInput(attrs={'accept': '*/*'}),  # Allow all file types
            'cover_letter': forms.ClearableFileInput(attrs={'accept': '*/*'})  # Allow all file types
        }

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            # Optional: Validate file type if needed
            return cv
        return cv

    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        if cover_letter:
            # Optional: Validate file type if needed
            return cover_letter
        return cover_letter
