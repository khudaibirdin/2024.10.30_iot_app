from datetime import datetime


class ClassGetValuesFromVegaParcel:
    """
    Класс в котором конкретно происходит разделение сырых данных от Vega Server на значения переменных
    """
    def __init__(self):
        pass

    def convert(self, sensor_type, variable_type, raw_data):
        match sensor_type:
            case "ДТ":
                if len(raw_data) == 20:
                    data, battery = self.DT_convert(variable_type, raw_data)
                else:
                    return None, None
            case "ДиВх": 
                if len(raw_data) == 30:
                    data, battery = self.DI_convert(variable_type, raw_data)
                else:
                    return None, None
            case "RTU": 
                data, battery = self.RTU_convert(variable_type, raw_data)
        return data, battery
    
    def DT_convert(self, variable_type, raw_data):
        """
        Декодирование информации от датчика Вега ТЛ-11
        """
        match variable_type:
            case "Датчик":
                data = data = float(f"{self._swap_decode_temp(raw_data[10:14])}")# C, {self._swap_decode_temp(data[14:18])} C" # C*10
            case "Термощуп":
                data = float(f"{self._swap_decode_temp(raw_data[14:18])}")
        return data, str(int(raw_data[0:2], 16))+" %"
    
    def DI_convert(self, variable_type, raw_data):
        """
        Декодирование информации от датчика СИ-13-485 в режиме дискретных вводов
        """
        def DiVh_from_data_to_variable(data, mask):
            return True if int(data, 16) & int(mask, 16) == int(mask, 16) else False
        match variable_type:
            case "Дискретный вход 1":
                data = raw_data[12:20]
                # time = self._swap_decode_time(raw_data[2:10])
                result = DiVh_from_data_to_variable(data, "01000000")  
            case "Дискретный вход 2":
                data = raw_data[20:28]
                # time = self._swap_decode_time(raw_data[2:10])
                result = DiVh_from_data_to_variable(data, "01000000")
        return result, None
    
    def RTU_convert(self, variable_type, raw_data):
        return None, None
    
    def _swap_decode_temp(self, data):
        '''
        Функция преобр. темп. из строки, смена байтов и декод в градусы
        '''
        data = int(data[2:4] + data[0:2], 16)/10
        if data > 6000:
            data = -(6553.5 - data)
        return round(data, 1)
    
    def _swap_decode_time(self, data):
        '''
        Функция преобр. времени из строки, смена байтов
        '''
        data = data[6:] + data[4:6] + data[2:4] + data[0:2]
        data = datetime.utcfromtimestamp(int(data, 16)+5*60*60).strftime('%d.%m.%Y %H:%M:%S')
        return data
    