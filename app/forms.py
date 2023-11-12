from django import forms
import json
from .models import Trip


class StartTrip(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ['destination_lat', 'destination_lon']

    origin_lat = forms.DecimalField(widget=forms.HiddenInput())
    origin_lon = forms.DecimalField(widget=forms.HiddenInput())
