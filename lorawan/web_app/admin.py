from django.contrib import admin

from web_app.models import Sensor
from web_app.models import Filial
from web_app.models import Location
from web_app.models import DiscreteVariable
from web_app.models import TemperatureSensorVariable

# Register your models here.

admin.site.register(Sensor)
admin.site.register(DiscreteVariable)
admin.site.register(TemperatureSensorVariable)
admin.site.register(Filial)
admin.site.register(Location)
