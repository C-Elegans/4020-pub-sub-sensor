import asyncio
import websockets
import requests
import re
import json
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

data = '{"cmd": "subscribe", "sensorid": "button"}'

button_event = asyncio.Event()
button_value = 0

smoke_event = asyncio.Event()
smoke_lock = asyncio.Lock()
is_smoke = False

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


async def update_smoke(smoke):
    global is_smoke
    async with smoke_lock:
        prev_smoke = is_smoke
    smoke = False if smoke == "false" else True
    print(smoke)
    if smoke != prev_smoke:
        is_smoke = smoke
        print("Notifying smoke_event")
        smoke_event.set()


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
                if key == 'SmokeDetector':
                    await update_smoke(value)
        await asyncio.sleep(1)





    

async def handle_logic():
    print("handle logic")
    while True:
        h = asyncio.ensure_future(smoke_event.wait())
        b = asyncio.ensure_future(button_event.wait())
        done, pending = await asyncio.wait({h, b},
                                           return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        # Handle fire detector value update or button press
        smoke_event.clear()
        async with smoke_lock:
            smoke = is_smoke
        if smoke:
            print("Fire!")
            PWM.start("P8_13", 25, 1000)
        else:
            if button_event.is_set():
                print("Reset!")
                PWM.stop("P8_13")
                PWM.cleanup()
                button_event.clear()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    handle_logic(),
    subscribe_to_n4abi(),
    poll_spencer()))
