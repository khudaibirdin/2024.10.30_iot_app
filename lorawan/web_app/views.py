from sys import platform
from pprint import pprint
from datetime import datetime
import time

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import web_app.service as service
from users.models import User
from web_app.models import Filial


# def history(func):
#     """
#     Декоратор для отслеживания какие сайты и когда посещают пользователи
#     """
#     def wrapper(*args, **kwargs):
#         history_path = "/root/history.txt" if platform == "linux" else "history.txt"
#         with open(history_path, "a") as file:
#             file.write(f"{str(datetime.now())}, {args[0].user}, {args[0].path}\n")
#         resp = func(*args, **kwargs)
#         return resp
#     return wrapper


@login_required(login_url='/page_auth/')
def page_about(request):
    """
    Cтраница о проекте (для описания того, зачем нужна эта система и немного о принципе работы)
    """
    return render(request, 'web_app/page_about.html')

@login_required(login_url='/page_auth/')
def page_sensors(request):
    """
    Страница главная по списку датчиков
    """
    # запрос о списке датчиков филиала В БДВП
    user = User.objects.get(username=request.user).filial.all()
    sensors_list = service.get_filial_sensors_list(user)
    view_data = {
        'sensors_data': sensors_list,
    }
    return render(request, 'web_app/page_sensors.html', context=view_data)

@login_required(login_url='/page_auth/')
def page_sensors_single(request):
    """
    Страница по одиночному датичку по get-запросу
    """
    if request.GET:
        sensor_name = request.GET.get("sensor")
        sensor_variables = service.get_sensor_variables(sensor_name)
        view_data = {
            "sensor_variables": sensor_variables
        }
        return render(request, 'web_app/page_sensors_single.html', context=view_data)

def page_not_found(request):
    """
    Cтраницa при переходе по неизвестному адресу
    """
    
    return HttpResponse('Page not found')

@login_required(login_url='/page_auth/')
def page_main(request):
    """
    Переадресация с главной страницы на страницу "Диспетчер устройств"
    """

    return redirect('/variables')

@login_required(login_url='/page_auth/')
def page_variables(request):
    """
    Страница с параметрами от датчиков
    """
    # получение филиалов пользователя (вдруг их много)
    user = User.objects.get(username=request.user).filial.all()
    # получение списка датчиков для этих филиалов
    sensors_list = service.get_filial_sensors_list(user)
    # запрос о списке переменных списка датчиков в БДВП
    sensors_variables_list = service.get_sensors_variables_list(sensors_list)
    # получить сырые значения переменных
    sensors_variables_raw_data = service.get_variables_last_raw_values(sensors_variables_list)
    # преобразовать сырые данные в значения переменных
    data = service.convert_raw_data_to_variables_values(sensors_variables_raw_data)
    # группировать список в словарь с группировкой по филиалу, объекту
    def group_sensors_by_filial_and_location(sensors_list):
        grouped_data = {}  # Инициализация обычного словаря

        for sensor in sensors_list:
            filial = sensor['filial']
            location = sensor['location']
            
            # Проверяем, существует ли филиал в словаре
            if filial not in grouped_data:
                grouped_data[filial] = {}  # Инициализируем новый словарь для филиала

            # Проверяем, существует ли объект в филиале
            if location not in grouped_data[filial]:
                grouped_data[filial][location] = []  # Инициализируем список для объекта

            # Добавляем датчик в список соответствующего объекта
            grouped_data[filial][location].append(sensor)

        return grouped_data
    
    data = group_sensors_by_filial_and_location(data)
    view_data = {
        "sensors_variables_data": data
    }
    return render(request, 'web_app/page_variables.html', context=view_data)

@login_required(login_url='/page_auth/')
def page_variables_single(request):
    """
    Страница с отдельной переменной
    """
    if request.GET:
        sensor_code = request.GET.get("sensor")
        variable_name = request.GET.get("variable")
        sensor_info = service.get_sensor_info(sensor_code)
        variable_info = service.get_variable_info(sensor_code, variable_name)
        period = [int(time.time()*1000 - 1000000000), int(time.time()*1000)]
        variable_history_data = service.get_variable_history_data(sensor_code, variable_name, period)
        if type(variable_history_data[0]["data"]) != bool:
            variable_graphic_data = [{"x": i["time"], "y": i["data"]} for i in variable_history_data]
        else:
            variable_graphic_data = [{"x": i["time"], "y": 1 if i["data"] == True else 0} for i in variable_history_data]
        view_data = {
            "sensor_info": sensor_info,
            "variable_info": variable_info,
            "variable_history_data": variable_history_data,
            "variable_graphic_data": variable_graphic_data,
        }
        return render(request, 'web_app/page_variables_single.html', context=view_data)

@login_required(login_url='/page_auth/') 
def page_variables_single_post(request):
    """
    Обработка POST-запроса при вводе интервала времени и нажатии кнопки для отображения данных с датчиков.
    """
    if request.POST:
        # получение кода датчика из get-запроса
        sensor_code = request.POST.get("sensor")
        variable_name = request.POST.get("variable")
        sensor_info = service.get_sensor_info(sensor_code)
        variable_info = service.get_variable_info(sensor_code, variable_name)
        time_today = int(time.time()*1000)
        try:
            period_begin = int(datetime.strptime(request.POST.get("date_begin"),'%Y-%m-%d').timestamp()*1000)
        except Exception as E:
            print(E)
            period_begin = time_today - 1000000000
        try:
            period_end = int(datetime.strptime(request.POST.get("date_end"),'%Y-%m-%d').timestamp()*1000)
        except Exception as E:
            print(E)
            period_end = time_today
        period = [period_begin, period_end]
        variable_history_data = service.get_variable_history_data(sensor_code, variable_name, period=period)
        if type(variable_history_data[0]["data"]) != bool:
            variable_graphic_data = [{"x": i["time"], "y": i["data"]} for i in variable_history_data]
        else:
            variable_graphic_data = [{"x": i["time"], "y": 1 if i["data"] else 0} for i in variable_history_data]
        view_data = {
            "sensor_info": sensor_info,
            "variable_info": variable_info,
            "variable_history_data": variable_history_data,
            "variable_graphic_data": variable_graphic_data,
        }
        return render(request, 'web_app/page_variables_single.html', context=view_data)

def test(request):
    data = service.get_data_from_all_devices()
    messages = service.compare_data_and_emergency_settings(data)
    pprint(messages)
    service.create_journal_sign(messages)
    