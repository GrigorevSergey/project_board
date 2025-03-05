from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    name = models.CharField(max_length=20, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
