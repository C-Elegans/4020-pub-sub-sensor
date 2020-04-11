from flask import Flask, request, abort


PORT = 9000
app = Flask(__name__)


class SensorData:
    def __init__(self, stype, name, value):
        self.stype = stype
        self.name = name
        self.value = value


class AppData:
    def __init__(self):
        self.sensors = {}

    def update_sensor(self, stype, name, value):
        self.sensors[name] = SensorData(stype, name, value)

appdata = AppData()

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/sensor', methods=['POST', 'PUT'])
def update_sensor():
    print(request.json)
    if not request.json:
        abort(400)
    if 'sensorid' not in request.json:
        abort(400)
    if 'sensortype' not in request.json:
        abort(400)
    if 'value' not in request.json:
        abort(400)
    sid = request.json.get('sensorid')
    stype = request.json.get('sensortype')
    value = request.json.get('value')
    appdata.update_sensor(stype, sid, value)
    return "OK"


if __name__ == '__main__':
    app.run(debug=False, port=PORT)
