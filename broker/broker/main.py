from quart import Quart, request, abort, jsonify
from broker.appdata import AppData
import jwt


PORT = 9000
app = Quart(__name__)



appdata = AppData()

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/sensor', methods=['POST', 'PUT'])
async def update_sensor():
    data = await request.get_data()
    # Note, DO NOT USE EXCEPT TO GET KEY
    claimset = jwt.decode(data, verify=False, algorithms=['RS256'])
    if not claimset:
        abort(400)
    if 'sensorid' not in claimset:
        abort(400)
    pub_key = appdata.keys.get_public_key(claimset['sensorid'])

    data = jwt.decode(data, pub_key, algorithms=['RS256'])
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
    appdata.start_publisher_server()
    app.run(debug=False, port=PORT)
