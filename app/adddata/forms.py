from django.forms import ModelForm

from app.adddata.models import CatchFish


class CatchFishForm(ModelForm):
    class Meta:
        model = CatchFish
        exclude = ("fisherman",)
