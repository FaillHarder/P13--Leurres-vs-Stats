from django.db import models
from django.contrib.auth import get_user_model

from PIL import Image


# Create your models here.
class Profile(models.Model):

    AVATAR_SIZE = (600, 600)

    user = models.OneToOneField(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
    pseudo = models.CharField(max_length=50, verbose_name="Pseudo")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Prénom")
    name = models.CharField(max_length=50, blank=True, verbose_name="Nom")
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)

    def resize_avatar(self):
        try:
            avatar = Image.open(self.avatar)
            avatar.thumbnail(self.AVATAR_SIZE)
            avatar.save(self.avatar.path)
        except ValueError:
            pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_avatar()

    def __str__(self) -> str:
        return self.pseudo
