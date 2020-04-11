from broker.keys import Keys
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

    def update_sensor(self, stype, name, value):
        self.sensors[name] = SensorData(stype, name, value)

    def get_all_sensors(self):
        lst = list(self.sensors.values())
        return [x.json() for x in lst]
