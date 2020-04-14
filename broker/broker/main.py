from quart import Quart, request, abort, jsonify, websocket
from broker.appdata import AppData
from functools import wraps
import asyncio
import jwt
import json


PORT = 9000
app = Quart(__name__)



appdata = AppData()
appdata.keys.load_keys_from_directory('keys/')
print(appdata.keys._private_keys)


def collect_websocket(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        queue = asyncio.Queue()
        appdata.connected_websockets.add(queue)
        try:
            return await func(queue, *args, **kwargs)
        finally:
            appdata.connected_websockets.remove(queue)
    return wrapper

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
    await appdata.update_sensor(stype, sid, value)
    return "OK"

@app.websocket('/api/subscribe')
@collect_websocket
async def ws(queue):
    data = await websocket.receive()
    data = json.loads(data)
    if not data:
        await websocket.send('{"status": "error"}')
        return

    requested_id = None
    if 'sensorid' in data:
        requested_id = data['sensorid']
    requested_type = None
    if 'sensortype' in data:
        requested_type = data['sensortype']
    while True:
        msg = await queue.get()
        if requested_id and msg['sensorid'] != requested_id:
            continue
        if requested_type and msg['sensortype'] != requested_type:
            continue
        msg = json.dumps(msg)
        await websocket.send(msg)

@app.route('/api/sensor', methods=['GET'])
def get_sensor():
    data = appdata.get_all_sensors()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=False, port=PORT)
