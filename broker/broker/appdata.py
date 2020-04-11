from broker.keys import Keys
import asyncio
import json

SOCKET_PORT = 9001


class SensorData:
    def __init__(self, stype, name, value):
        self.stype = stype
        self.name = name
        self.value = value

    def json(self):
        return {"sensorid": self.name,
                "sensortype": self.stype,
                "value": self.value}


class AppData:
    def __init__(self):
        self.sensors = {}
        self.keys = Keys()
        self.ws_thread = None
        self.connected_websockets = set()

    async def update_sensor(self, stype, name, value):
        self.sensors[name] = sensor = SensorData(stype, name, value)
        for queue in self.connected_websockets:
            await queue.put(sensor.json())

    def get_all_sensors(self):
        lst = list(self.sensors.values())
        return [x.json() for x in lst]
