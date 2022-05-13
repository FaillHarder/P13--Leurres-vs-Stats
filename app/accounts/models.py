from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
    pseudo = models.CharField(max_length=50, verbose_name="Pseudo")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Prénom")
    name = models.CharField(max_length=50, blank=True, verbose_name="Nom")
    avatar = models.ImageField(default="giphy_python.gif", upload_to='avatar/', null=True, blank=True)

    def __str__(self) -> str:
        return self.pseudo
