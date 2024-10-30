import json

from websocket import create_connection


class ClassWebsocketActions:
    def __init__(self):
        pass
    # подключение к websocket и отключение от websocket
    def _connect(self, address):
        connection = create_connection(address)
        return connection

    # октлючиться от websocket
    def _disconnect(self, connection):
        connection.close()
        pass


class ClassDataFromLoRaServer(ClassWebsocketActions):
    def __init__(self, configuration):
        self.ws_address = configuration["websocket"]["address"]
        self.user = configuration["vega_lorawan_user"]
        self.ws_connection = None
    
    def _send_parcel(self, parcel):
        self.ws_connection.send(json.dumps(parcel))

    def _login(self):
        self.ws_connection = self._connect(self.ws_address)
        parcel = {
            "cmd": "auth_req",
            "login": self.user["login"],
            "password": self.user["password"]
        }
        self._send_parcel(parcel)
    
    def _logout(self):
        self._disconnect(self.ws_connection)
    
    def _get_responce(self):
        data = self.ws_connection.recv()
        return json.loads(data)
    
    def communicate(self, parcel):
        self._login()
        self._get_responce()
        self._send_parcel(parcel)
        data = self._get_responce()
        self._logout()
        return data

