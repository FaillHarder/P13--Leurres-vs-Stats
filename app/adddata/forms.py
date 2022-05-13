from app.adddata.models import CatchFish

from django.forms import ModelForm


class CatchFishForm(ModelForm):
    class Meta:
        model = CatchFish
        fields = ['lure', 'color_lure', 'sky_state', 'water_state', ]
        exclude = ("fisherman",)
