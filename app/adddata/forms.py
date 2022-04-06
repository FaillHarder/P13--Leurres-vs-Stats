from django.forms import ModelForm

from app.adddata.models import CatchFish


class CatchFishForm(ModelForm):
    class Meta:
        model = CatchFish
        fields = ['lure', 'color_lure', 'sky_state', 'water_state', ]
        exclude = ("fisherman",)
