import asyncio
import websockets
import json
import random

async def simulate_device(device_id):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "type": "AUTH",
            "payload": {"token": "abc123"}
        }))
        await asyncio.sleep(1)

        for i in range(5):
            telemetry = {
                "type": "TELEMETRY",
                "payload": {
                    "device_id": device_id,
                    "temperature": round(20 + random.random() * 5, 1),
                    "humidity": round(40 + random.random() * 10, 1),
                    "battery": 100 - i * 2
                }
            }
            await websocket.send(json.dumps(telemetry))
            await asyncio.sleep(2)

async def main():
    await asyncio.gather(
        simulate_device("device001"),
        simulate_device("device002"),
        simulate_device("device003")
    )

asyncio.run(main())
