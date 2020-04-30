import asyncio
import websockets
import requests
import re
import json

data = '{"cmd": "subscribe", "sensorid": "button"}'

button_event = asyncio.Event()
button_value = 0

heat_event = asyncio.Event()
heat_lock = asyncio.Lock()
heat_value = 0

async def subscribe_to_n4abi():
    global button_value
    uri = "ws://n4abi.com:9000/api/subscribe"
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        while True:
            resp = await websocket.recv()
            jdata = json.loads(resp)
            status = jdata['value']
            prev_value = button_value
            value = 1 if status == 'pressed' else 0
            button_value = value
            if value == 1 and prev_value == 0:
                print("Notifying button_event")
                button_event.set()


async def update_heat(heat):
    global heat_value
    async with heat_lock:
        prev_heat = heat_value
    heat = float(heat)
    print(heat)
    if prev_heat != heat:
        heat_value = heat
        print("Notifying heat_event")
        heat_event.set()


async def poll_spencer():
    uri = "http://73.43.115.119:49999/api/subscribe"
    loop = asyncio.get_event_loop()
    while True:
        fut = loop.run_in_executor(None, requests.get, uri)
        resp = await fut
        data = resp.text
        data = data.replace('Sensors:\n\n', '')
        #print(data)
        lines = data.splitlines()
        for line in lines:
            if line:
                key, value = line.split(':')
                if key == 'ProfessionalThermistor':
                    await update_heat(value)
        await asyncio.sleep(1)





    

async def handle_logic():
    print("handle logic")
    while True:
        h = asyncio.ensure_future(heat_event.wait())
        b = asyncio.ensure_future(button_event.wait())
        done, pending = await asyncio.wait({h, b},
                                           return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        # Handle fire detector value update or button press
        heat_event.clear()
        async with heat_lock:
            heat = heat_value
        if heat > 80:
            print("Fire!")
        else:
            if button_event.is_set():
                print("Reset!")
        button_event.clear()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    handle_logic(),
    subscribe_to_n4abi(),
    poll_spencer()))
