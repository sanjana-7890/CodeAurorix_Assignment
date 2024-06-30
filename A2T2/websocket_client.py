import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:5000/socket.io/?transport=websocket"
    async with websockets.connect(uri) as websocket:
        # Send URL to initiate session
        await websocket.send(json.dumps({"url": "https://ums.lpu.in/lpuums/"}))
        response = await websocket.recv()
        print("Received:", response)

        # Send get_info operation
        await websocket.send(json.dumps({"operation": "get_info"}))
        response = await websocket.recv()
        print("Received:", response)

        # Send get_subdomains operation
        await websocket.send(json.dumps({"operation": "get_subdomains"}))
        response = await websocket.recv()
        print("Received:", response)

        # Send get_asset_domains operation
        await websocket.send(json.dumps({"operation": "get_asset_domains"}))
        response = await websocket.recv()
        print("Received:", response)

asyncio.get_event_loop().run_until_complete(test_websocket())
