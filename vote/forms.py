from django import forms
from .validators import zip_code_validator
from .models import AgeRange


class VoterRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    age_range = forms.ModelChoiceField(queryset=AgeRange.objects.all(), empty_label='Age Range')
    zip_code = forms.CharField(max_length=5)

