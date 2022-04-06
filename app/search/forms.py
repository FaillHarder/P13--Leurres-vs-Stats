from django import forms

from app.adddata.models import SkyState, WaterState


class SearchForm(forms.Form):
    skystate = forms.ModelChoiceField(
        queryset=SkyState.objects.all(),
        initial=1,
        required=True
    )
    waterstate = forms.ModelChoiceField(
        queryset=WaterState.objects.all(),
        initial=1,
        required=True
    )
