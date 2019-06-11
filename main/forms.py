from django import forms

from main.models import Renter

class RenterForm(forms.ModelForm):

    class Meta:
        model = Renter
        exclude = ('landlord','token','last_paid')
