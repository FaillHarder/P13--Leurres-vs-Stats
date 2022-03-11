from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={"unique": "Cette adresse mail existe déjà"}
    )
    username = models.CharField(null=True, max_length=30)
    # Login with email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
