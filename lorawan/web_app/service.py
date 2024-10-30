from pprint import pprint

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from web_app.classes.DataFromLoRaServer import *
from web_app.classes.DataBaseJournal import *
from web_app.classes.VegaDevices import *
from web_app.classes.GetValuesFromVegaParcel import *

from web_app.models import Sensor
from web_app.models import DiscreteVariable
from web_app.models import TemperatureSensorVariable
from users.models import User
from web_app.models import Filial



@receiver(pre_save, sender=Sensor)
def sensor_save_handler(instance, **kwargs):
    """
    При добавлении НОВОГО датчика будет выполняться то, что в исключении.
    Оставить на потом, т.к. придется прописывать DevEui в форме заполнения модели в админ-панели
    """

    try:
        previous = Sensor.objects.get(code=instance.code)
    except Sensor.DoesNotExist:
        print(instance.id, instance.filial, instance.code)

def get_journal_data(request, journal_path):
    """
    Получение строк таблицы с бд журнала по филиалу пользователя
    """

    try:
        user = User.objects.filter(username=request.user)
        for i in user:
            user_filial = i.filial
        db = СlassDataBaseJournal(journal_path)
        journal = reversed(db.take_signs_by_condition('journal', f'where filial="{user_filial}"'))
    except Exception as E:
        print(E)
        journal = None
    return journal

def get_sensors_variables_list(sensors_list):
    """
    Получение списка переменных для списка датчиков
    """
    variables_list = []
    for sensor in sensors_list:
        data = get_sensor_variables(sensor["code"])
        for i in data:
            temp = sensor.copy()
            temp["variable"] = i
            variables_list.append(temp)
    return variables_list
    
def get_sensor_variables(sensor_name):
    """
    Получение списка переменных для одного датчика
    """

    # запрос в БДВП узнать тип датчика
    sensor = Sensor.objects.get(code=sensor_name)
    sensor_type = sensor.type

    result = []
    variables_list = []

    match sensor_type:
        case "ДиВх":
            variables = DiscreteVariable.objects.filter(sensor=sensor.id)
            for i in variables:
                variables_list.append({"parent_sensor": i.sensor.code,
                                       "parameter_name": i.parameter_name,
                                       "type": i.type,
                                       "alarm":i.alarm})
        case "ДТ":
            variables = TemperatureSensorVariable.objects.filter(sensor=sensor.id)
            for i in variables:
                variables_list.append({"parent_sensor": i.sensor.code,
                                       "parameter_name": i.parameter_name,
                                       "type": i.type,
                                       "unit": i.unit,
                                       "HH":i.HH,
                                       "LL":i.LL})
        case "485RTU": pass
    return variables_list

def get_filial_sensors_list(filial):
    """
    Получение списка датчиков по филиалу
    """
    sensors = Sensor.objects.filter(filial__in=filial)
    sensors_list = []
    for sensor in sensors:
        sensors_list.append({"code": sensor.code, "filial": sensor.filial.filial, "location": sensor.location.location, "information": sensor.information, "type": sensor.type, "devEui": sensor.devEui})
    return sensors_list

def get_variables_last_raw_values(sensors_variables_list):
    """
    Добавление значений переменных к структуре
    """
    lora = ClassDataFromLoRaServer(settings.USER_SETTINGS)
    for sensor in sensors_variables_list:
        parcel = {
            "cmd": "get_data_req",
            "devEui":sensor["devEui"],
            "select": {
                "limit": 1,
                "port": 2
            }
        }
        sensor["raw_value"] = lora.communicate(parcel=parcel)["data_list"][0]["data"]
        time = lora.communicate(parcel=parcel)["data_list"][0]["ts"]
        sensor["time"] = datetime.fromtimestamp(int(time/1000)+5*60*60).strftime('%d.%m.%Y %H:%M:%S')
    return sensors_variables_list

def convert_raw_data_to_variables_values(raw_data):
    converter = ClassGetValuesFromVegaParcel()
    for sensor in raw_data:
        res, battery = converter.convert(sensor["type"], sensor["variable"]["type"], sensor["raw_value"])
        if res != None:
            sensor["variable"].update({"data":res})
        if battery != None:
            sensor.update({"battery": battery})
    return raw_data

def get_variable_history_data(sensor_code, variable_name, period):
    sensor_devEui = Sensor.objects.get(code=sensor_code).devEui
    sensor_type = Sensor.objects.get(code=sensor_code).type
    match sensor_type:
        case "ДиВх": variable_type = DiscreteVariable.objects.filter(parameter_name=variable_name)[0].type
        case "ДТ": variable_type = TemperatureSensorVariable.objects.filter(parameter_name=variable_name)[0].type
    data_list = []
    converter = ClassGetValuesFromVegaParcel()
    data = get_sensor_period_history_data(sensor_devEui, period)
    for i in data:
        data_list.append({"data": converter.convert(sensor_type, variable_type, i[0])[0], "time":datetime.fromtimestamp(int(i[1]/1000)+5*60*60).strftime('%d.%m.%Y %H:%M:%S')})
    return data_list

def get_sensor_period_history_data(sensor_devEui, period):
    lora = ClassDataFromLoRaServer(settings.USER_SETTINGS)
    parcel = {
        "cmd": "get_data_req",
        "devEui":sensor_devEui,
        "select": {
            "date_from": period[0],
            "date_to": period[1],
            "port": 2
        }
    }
    data_obj = lora.communicate(parcel=parcel)["data_list"]
    data_list = [[sign["data"], sign["ts"]] for sign in data_obj]
    return data_list

def get_sensor_amount_history_data(sensor_devEui, limit):
    lora = ClassDataFromLoRaServer(settings.USER_SETTINGS)
    parcel = {
        "cmd": "get_data_req",
        "devEui":sensor_devEui,
        "select": {
            "limit": limit,
            "port": 2
        }
    }
    data_obj = lora.communicate(parcel=parcel)["data_list"]
    data_list = [[sign["data"], sign["ts"]] for sign in data_obj]
    return data_list

def get_sensor_info(sensor_code):
    sensor_data = Sensor.objects.get(code=sensor_code)
    return sensor_data

def get_variable_info(sensor_code, variable_name):
    sensor = Sensor.objects.get(code=sensor_code)
    try:
        variable = TemperatureSensorVariable.objects.get(sensor=sensor.id, parameter_name=variable_name)
        return variable
    except TemperatureSensorVariable.DoesNotExist:
        pass
    try:
        variable = DiscreteVariable.objects.get(sensor=sensor.id, parameter_name=variable_name)
        return variable
    except DiscreteVariable.DoesNotExist:
        pass

def get_data_from_all_devices():
    """
    Тестовая функция
    Получение крайних данных и информации от датчиков со всех филиалов
    """
    sensors_list = []
    sensors = Sensor.objects.all()
    for sensor in sensors:
        sensors_list.append({"code": sensor.code, "filial": sensor.filial, "location": sensor.location, "information": sensor.information, "type": sensor.type, "devEui": sensor.devEui})
    for sensor in sensors_list:
        data = get_sensor_variables(sensor["code"])
        sensor["variables"] = data
    sensors_variables_raw_data = get_variables_last_raw_values(sensors_list)
    # преобразовать сырые данные в значения переменных
    data = convert_raw_data_to_variables_values(sensors_variables_raw_data)
    return data