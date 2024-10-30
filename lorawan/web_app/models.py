from django.db import models


class Filial(models.Model):
    filial = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.filial}"

class Location(models.Model):
    location = models.CharField(max_length=250)
    filial = models.ForeignKey(Filial, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.filial, self.location}"
    
class Sensor(models.Model):
    """
    Модель датчиков с описанием всех параметров
    """

    filial = models.ForeignKey(Filial, on_delete = models.CASCADE)
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    devEui = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=[("ДТ","ДТ"), ("ДиВх","ДиВх"), ("485RTU","485RTU")]) # Датчик температуры, модуль дискретного ввода, модуль ModbusRTU и т.д.
    information = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.code}, {self.filial}, {self.location}"


class DiscreteVariable(models.Model):
    """
    Модель дикретной переменной для датчика СИ-13-485 работающего в режиме охранный для 2-х входов
    """

    filial = models.ForeignKey(Filial, on_delete = models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete = models.CASCADE)
    parameter_name = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=[("Дискретный вход 1", "Дискретный вход 1"), ("Дискретный вход 2", "Дискретный вход 2")])
    alarm = models.BooleanField()

    def __str__(self):
        return f"{self.filial}, {self.sensor}, {self.parameter_name}"


class TemperatureSensorVariable(models.Model):
    """
    Модель переменных с датчика температуры ТЛ-11
    """

    filial = models.ForeignKey(Filial, on_delete = models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete = models.CASCADE)
    parameter_name = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=[("Датчик", "Датчик"), ("Термощуп", "Термощуп")])
    unit = models.CharField(max_length=250)
    HH = models.FloatField()
    LL = models.FloatField()

    def __str__(self):
        return f"{self.filial}, {self.sensor}, {self.parameter_name}"
    