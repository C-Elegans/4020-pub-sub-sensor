from broker.keys import Keys
import asyncio
import websockets
import json
import threading

SOCKET_PORT = 9001


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
        self.ws_thread = None

    def update_sensor(self, stype, name, value):
        self.sensors[name] = SensorData(stype, name, value)

    def get_all_sensors(self):
        lst = list(self.sensors.values())
        return [x.json() for x in lst]

    async def hello(self, websocket, path):
        _ = await websocket.recv()
        await websocket.send("Hello!")

    def start_publisher_server(self):

        def thread_fun():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print("Starting server")
            server = websockets.serve(self.hello, "", SOCKET_PORT)
            print("Async loop")
            asyncio.get_event_loop().run_until_complete(server)
            asyncio.get_event_loop().run_forever()
        self.ws_thread = threading.Thread(target=thread_fun, daemon=True)
        self.ws_thread.start()


