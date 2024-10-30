from django.db import models
from django.contrib.auth.models import AbstractUser

from web_app.models import Filial
# Create your models here.

class User(AbstractUser):
    """
    Модель пользователя.
    """
    use_in_migrations = True
    username = models.CharField(editable=True, max_length=150, unique=True, verbose_name='username')
    password = models.CharField(editable=True, max_length=128, verbose_name='password')
    first_name = models.CharField(editable=True, max_length=100)
    last_name = models.CharField(editable=True, max_length=100)
    filial = models.ManyToManyField(Filial)
    department = models.CharField(editable=True, max_length=100)