from quart import Quart, request, abort, jsonify, websocket
from broker.appdata import AppData
from functools import wraps
import asyncio
import jwt
import json
import os


PORT = 9000
app = Quart(__name__)


file_dir = os.path.dirname(os.path.realpath(__file__))

appdata = AppData()
appdata.keys.load_keys_from_directory(os.path.join(file_dir, 'keys'))
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


async def send_if_matches(msg, requested_id, requested_type, websocket):
    if requested_id and msg['sensorid'] != requested_id:
        return
    if requested_type and msg['sensortype'] != requested_type:
        return
    msg = json.dumps(msg)
    await websocket.send(msg)


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

    initial_values = appdata.get_all_sensors()
    for msg in initial_values:
        await send_if_matches(msg, requested_id, requested_type,
                              websocket)
    while True:
        msg = await queue.get()
        await send_if_matches(msg, requested_id, requested_type,
                              websocket)

@app.route('/api/sensor', methods=['GET'])
def get_sensor():
    data = appdata.get_all_sensors()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=False, port=PORT)
