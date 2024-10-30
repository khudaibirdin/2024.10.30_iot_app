from django.db import models
from web_app.models import Filial
from web_app.models import Location
# Create your models here.


class Journal(models.Model):
    """
    Модель журнала сообщений
    """
    
    date = models.CharField(max_length=250)
    filial = models.ForeignKey(Filial, on_delete = models.CASCADE)
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    code = models.CharField(max_length=250)
    variable_name = models.CharField(max_length=250)
    message = models.CharField(max_length=250)