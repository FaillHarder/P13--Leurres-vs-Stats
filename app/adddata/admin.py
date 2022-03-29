from django.contrib import admin

from app.adddata.models import Color, Lure, CatchFish, SkyState, WaterState


# Register your models here.
admin.site.register(Color)
admin.site.register(Lure)
admin.site.register(CatchFish)
admin.site.register(SkyState)
admin.site.register(WaterState)
