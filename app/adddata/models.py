from django.conf import settings
from django.db import models


# Create your models here.
class Lure(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Leurre")
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Couleur du leurre")
    image = models.ImageField(upload_to="color_lure", blank=True, null=True)

    def __str__(self):
        return self.name


class CatchFish(models.Model):
    CLEAR = 'Clair'
    TROUBLED = 'Trouble'
    WATER_CHOICES = [
        (CLEAR, 'Clair'),
        (TROUBLED, 'Trouble')
    ]

    SUNNY = 'Ensoleillé'
    WHITE = 'Blanc'
    GREY = 'Gris'
    BLACK = 'Noir'
    SKY_CHOICES = [
        (SUNNY, 'Ensoleillé'),
        (WHITE, 'Blanc'),
        (GREY, 'Gris'),
        (BLACK, 'Noir')
    ]

    fisherman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Pécheur")
    lure = models.ForeignKey(Lure, on_delete=models.CASCADE, verbose_name="Leurre")
    color_lure = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Couleur du leurre")
    sky_state = models.CharField(max_length=30, choices=SKY_CHOICES, default=SUNNY, verbose_name='Etat du ciel')
    water_state = models.CharField(max_length=30, choices=WATER_CHOICES, default=CLEAR, verbose_name='Etat de l\'eau')

    def __str__(self) -> str:
        return f"({self.lure}/{self.color_lure}) (Ciel {self.sky_state}/Eau {self.water_state}). Pécheur : {self.fisherman}"
