import asyncio
import websockets
import requests
import re
import json
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

data = '{"cmd": "subscribe", "sensorid": "button"}'

# These variables communicate the status of the reset button and smoke
# detector to the process controlling the alarm. If the smoke detector
# or button status changes from false to true, the corresponding event
# is set which wakes up the alarm process
button_event = asyncio.Event()
button_value = False

smoke_event = asyncio.Event()
smoke_lock = asyncio.Lock()
is_smoke = False


# This function subscribes to the button sensor on our broker. It
# waits to receive button messages, and if the button status goes from
# false to true it sets button_event to wake up the alarm process
async def subscribe_to_n4abi():
    global button_value

    # connect to broker
    uri = "ws://n4abi.com:9000/api/subscribe"
    async with websockets.connect(uri) as websocket:
        # send the subscription message
        await websocket.send(data)
        while True:
            # wait for any messages
            resp = await websocket.recv()
            # parse them
            jdata = json.loads(resp)
            status = jdata['value']
            prev_value = button_value
            value = True if status == 'pressed' else False
            button_value = value
            # if there's a rising edge, set button_event
            if value == 1 and prev_value == 0:
                print("Notifying button_event")
                button_event.set()


# Helper process to handle updating the is_smoke and smoke_event
# variables from a smoke value
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


# Spencer's Broker only works by polling, and returns data of the
# format:
# Sensors:
#
# key:value
# key2:value2
# etc.
# This polls his server once per second and looks for changes on the
# SmokeDetector key. It calls update_smoke with the value, and
# update_smoke will set smoke_event if there is any change in value
async def poll_spencer():
    uri = "http://73.43.115.119:49999/api/subscribe"
    loop = asyncio.get_event_loop()
    while True:
        fut = loop.run_in_executor(None, requests.get, uri)
        resp = await fut
        data = resp.text
        data = data.replace('Sensors:\n\n', '')
        lines = data.splitlines()
        for line in lines:
            if line:
                key, value = line.split(':')
                if key == 'SmokeDetector':
                    await update_smoke(value)
        await asyncio.sleep(1)


# This process handles turning on/off the alarm from the data
# variables above. It waits for one of the two events, and updates the
# alarm depending on what happened
async def handle_alarm():
    while True:
        # Wait for one of the two events
        h = asyncio.ensure_future(smoke_event.wait())
        b = asyncio.ensure_future(button_event.wait())
        done, pending = await asyncio.wait({h, b},
                                           return_when=asyncio.FIRST_COMPLETED)
        # Cancel the other waiting task
        for task in pending:
            task.cancel()

        # If there is smoke, set the alarm
        smoke_event.clear()
        async with smoke_lock:
            smoke = is_smoke
        if smoke:
            print("Fire!")
            PWM.start("P8_13", 25, 1000)
        else:
            # Otherwise, check to see if the button has been pressed,
            # and if so clear the alarm
            if button_event.is_set():
                print("Reset!")
                PWM.stop("P8_13")
                PWM.cleanup()
                button_event.clear()


# Start the 3 processes above
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    handle_alarm(),
    subscribe_to_n4abi(),
    poll_spencer()))
