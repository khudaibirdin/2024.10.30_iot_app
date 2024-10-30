from datetime import datetime, timedelta

from web_app.models import Filial
from journal.models import Journal



def get_all_filial_journal_signs(filial, amount=None):
    """
    Функция получения всех записей из БД Журнал для конкретного филиала
    """
    journal = Journal.objects.filter(filial__in=filial).order_by('-id')[:amount]
    journal_list = []
    for journal_sign in journal:
        journal_list.append(
            {"code": journal_sign.code,
             "date": journal_sign.date,
             "filial": journal_sign.filial,
             "location": journal_sign.location,
             "variable_name": journal_sign.variable_name,
             "message": journal_sign.message})
    return journal_list

def compare_data_and_emergency_settings(data):
    """
    Функция сравнения текущих данных и уставок
    """
    messages = []
    for sensor in data:
        for variable in sensor["variables"]:
            if "HH" in variable or "LL" in variable: # если параметр - аналоговый
                if variable["data"] >= variable["HH"]:
                    status = "высокий уровень"
                    variable["message"] = status
                    messages.append(sensor)
                elif variable["data"] <= variable["LL"]:
                    status = "низкий уровень"
                    variable["message"] = status
                    messages.append(sensor)
            elif "alarm" in variable: # если параметр - дискретный
                if variable["data"] == variable["alarm"]:
                    status = "авария"
                    variable["message"] = status
                    messages.append(sensor)
    return messages

def create_journal_sign(data):
    """
    Функция создания записи сообщения в таблицу БД Журнал
    """
    for sensor in data:
        for variable in sensor["variables"]:
            if "message" in variable:
                Journal.objects.create(
                    date=(datetime.now()).strftime("%d.%m.%Y %H:%M:%S"),
                    filial=sensor["filial"],
                    location=sensor["location"],
                    code=sensor["code"],
                    variable_name=variable["parameter_name"],
                    message=variable["message"]
                )