from flask import Flask, request, abort, jsonify
from broker.appdata import AppData
import jwt


PORT = 9000
app = Flask(__name__)



appdata = AppData()

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/sensor', methods=['POST', 'PUT'])
def update_sensor():
    # Note, DO NOT USE EXCEPT TO GET KEY
    claimset = jwt.decode(request.data, verify=False, algorithms=['RS256'])
    if not claimset:
        abort(400)
    if 'sensorid' not in claimset:
        abort(400)
    pub_key = appdata.keys.get_public_key(claimset['sensorid'])

    data = jwt.decode(request.data, pub_key, algorithms=['RS256'])
    if not data:
        abort(400)
    if 'sensortype' not in data:
        abort(400)
    if 'value' not in data:
        abort(400)
    sid = data['sensorid']
    stype = data['sensortype']
    value = data['value']
    appdata.update_sensor(stype, sid, value)
    return "OK"


@app.route('/api/sensor', methods=['GET'])
def get_sensor():
    data = appdata.get_all_sensors()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=False, port=PORT)
