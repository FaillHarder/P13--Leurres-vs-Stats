from django.conf import settings
from django.db import models


# Create your models here.
class Lure(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Leurre")
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name.title()


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Couleur du leurre")
    image = models.ImageField(upload_to="color_lure", blank=True, null=True)

    def __str__(self):
        return self.name.title()


class SkyState(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name.title()


class WaterState(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name.title()


class CatchFish(models.Model):

    fisherman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Pécheur")
    lure = models.ForeignKey(Lure, on_delete=models.CASCADE, verbose_name="Leurre")
    color_lure = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Couleur du leurre")
    sky_state = models.ForeignKey(SkyState, on_delete=models.CASCADE, verbose_name="Etat du ciel")
    water_state = models.ForeignKey(WaterState, on_delete=models.CASCADE, verbose_name="Etat de l'eau")

    def __str__(self) -> str:
        return f"({self.lure}/{self.color_lure}) (Ciel {self.sky_state}/Eau {self.water_state}). Pécheur : {self.fisherman}"
