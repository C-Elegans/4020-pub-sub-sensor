import asyncio
import websockets

async def test():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri) as websocket:
        await websocket.send("test")
        resp = await websocket.recv()
        print(resp)

asyncio.get_event_loop().run_until_complete(test())
