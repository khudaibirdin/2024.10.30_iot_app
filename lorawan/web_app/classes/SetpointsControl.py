from datetime import datetime
from DataBaseJournal import ClassDataBaseJournal


class ClassSetpointsJournal(ClassDataBaseJournal):
    """
    Класс для контроля уставок и формирования записей в журнал
    """
    def __init__(self):
        pass

    def control_setpoints(self, data):
        journal_massive = []
        for key, data in data.items():
            for key1, data1 in data.items():
                for key2, data2 in data1.items():
                    if data2['data']['data'] > data2['information']['highhigh']:
                        info = 'Прев. авар. уставки'
                        journal_massive.append([datetime.now().strftime("%d.%m.%Y %H:%M:%S"), key, key1, key2, info])
                        continue
                    if data2['data']['data'] > data2['information']['high']:
                        info = 'Прев. пред. уставки'
                        journal_massive.append([datetime.now().strftime("%d.%m.%Y %H:%M:%S"), key, key1, key2, info])
        return journal_massive
    