import asyncio
import websockets
import requests
import re

data = '{"cmd": "subscribe", "sensorid": "button"}'

button_event = asyncio.Event()

heat_event = asyncio.Event()
heat_lock = asyncio.Lock()
heat_value = 0

async def subscribe_to_n4abi():
    uri = "ws://n4abi.com:9000/api/subscribe"
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        while True:
            resp = await websocket.recv()
            print(resp)


async def update_heat(heat):
    global heat_value
    async with heat_lock:
        prev_heat = heat_value
    heat = float(heat)
    if prev_heat != heat:
        heat_value = heat
        print("Notifying heat_event")
        heat_event.set()


async def poll_spencer():
    uri = "http://localhost:8000/sensors.txt"
    loop = asyncio.get_event_loop()
    while True:
        fut = loop.run_in_executor(None, requests.get, uri)
        resp = await fut
        data = resp.text
        data = data.replace('Sensors:\n\n', '')
        print(data)
        lines = data.splitlines()
        for line in lines:
            if line:
                key, value = line.split(':')
                if key == 'heat':
                    await update_heat(value)
        await asyncio.sleep(1)



loop = asyncio.get_event_loop()
loop.run_until_complete(poll_spencer())
