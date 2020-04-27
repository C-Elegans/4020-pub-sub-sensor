import asyncio
import websockets

data = '{"cmd": "subscribe", "sensorid": "ex"}'

async def test():
    uri = "ws://localhost:9000/api/subscribe"
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        while True:
            resp = await websocket.recv()
            print(resp)

asyncio.get_event_loop().run_until_complete(test())
