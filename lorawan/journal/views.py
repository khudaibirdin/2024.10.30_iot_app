from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from journal.service import get_all_filial_journal_signs
from users.models import User

@login_required(login_url='/page_auth/')
def page_journal(request):
    """
    Страница Журнал
    """
    filial = User.objects.get(username=request.user).filial.all()
    journal = get_all_filial_journal_signs(filial, amount=20)
    def group_sensors_by_filial_and_location(sensors_list):
        grouped_data = {}  # Инициализация обычного словаря

        for sensor in sensors_list:
            filial = sensor['filial'].filial
            location = sensor['location'].location
            
            # Проверяем, существует ли филиал в словаре
            if filial not in grouped_data:
                grouped_data[filial] = {}  # Инициализируем новый словарь для филиала

            # Проверяем, существует ли объект в филиале
            if location not in grouped_data[filial]:
                grouped_data[filial][location] = []  # Инициализируем список для объекта

            # Добавляем датчик в список соответствующего объекта
            grouped_data[filial][location].append(sensor)

        return grouped_data
    journal_reformated = group_sensors_by_filial_and_location(journal)
    return render(request, 'journal/page_journal.html', context={"journal": journal_reformated})
