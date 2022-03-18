from django.db import models


# Create your models here.
class Lure(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to="color_lure", blank=True, null=True)

    def __str__(self):
        return self.name
