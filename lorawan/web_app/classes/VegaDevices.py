from datetime import datetime


class ClassVegaDecodeData:
    '''
    Класс для декодирования информации, получаемой с датчиков
    для каждого устройства описан свой метод
    и имеются вспомогательные методы для преобразований
    '''
    def __init__(self):
        pass
    
    def _Vega_TL_11(self, sensor_code, data):
        '''Декодирование информации от датчика Вега ТЛ-11'''
        bytes = [1, 4, 2, 2, 1]
        data_struct = {
            "code":  sensor_code,
            "battery": str(int(data[0:2], 16))+" %",   # %
            "time": self._swap_decode_time(data[2:10]),     # unixtime UTC
            "data": float(f"{self._swap_decode_temp(data[10:14])}")# C, {self._swap_decode_temp(data[14:18])} C" # C*10
        }
        return data_struct

    def _swap_decode_temp(self, data):
        '''Функция преобр. темп. из строки, смена байтов и декод в градусы'''
        data = int(data[2:4] + data[0:2], 16)/10
        return data
    
    def _swap_decode_time(self, data):
        '''Функция преобр. времени из строки, смена байтов'''
        data = data[6:] + data[4:6] + data[2:4] + data[0:2]
        data = datetime.utcfromtimestamp(int(data, 16)+5*60*60).strftime('%d.%m.%Y %H:%M:%S')
        return data
    
    # декодирование информации от датчика Вега СИ-13-485
    def _SI_13_485(self, sensor_code, data):
        print(data)
        bytes = [1, 4, 1, 2, 1, 1, 2]
        # 2 10 12 16 18 20 24
        data_struct = {
            "code": sensor_code,
            "battery": "24 В",
            "time": self._swap_decode_time(data[2:10]),
            "data": f"ModbusRTU: {data[26:-4]}"
        }
        return data_struct
    
    # в зависимости от типа датчика должно происходить соответствующее преобразование
    def get_data_by_device_type(self, user_devices_list,  user_devices_data):
        try:
            data_reformated = []
            for i in user_devices_data:
                devEui = i['devEui']
                for j in user_devices_list:
                    if devEui in j:
                        device_type = j[0]
                        match device_type:
                            case 'ДТ':
                                data = self._Vega_TL_11(j[2], i["data_list"][0]["data"])
                            case '485':
                                print(i)
                                data = self._SI_13_485(j[2], i["data_list"][0]["data"])
                        data_reformated.append(data)
        except Exception as E:
            print(E)
            data_reformated = None
            pass
        return data_reformated
    
    def reformat_all_data(self, sensor_type, data):
        data_reformated = []
        match sensor_type:
            case 'ДТ':
                for i in data[0]["data_list"]:
                    try:    # здесь это нужно т.к. бывает пустой массив и тогда косячат остальные функции
                        data_reformated.append(self._Vega_TL_11("", i["data"]))
                    except:
                        pass
            case '485':
                for i in data:
                    try:
                        data_reformated.append(self._SI_13_485("", i["data"]))
                    except:
                        pass
        return data_reformated
    