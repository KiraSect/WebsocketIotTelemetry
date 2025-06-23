import asyncio
import json
import websockets

connected_admins = set()
device_subscriptions = {}  # device_id -> set of admins

async def handler(websocket):
    try:
        token_validated = False
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get("type")
            payload = data.get("payload", {})

            if msg_type == "AUTH":
                token = payload.get("token")
                if token == "abc123":  # псевдо-проверка
                    token_validated = True
                    await websocket.send(json.dumps({"type": "AUTH_OK"}))
                else:
                    await websocket.send(json.dumps({"type": "ERROR", "payload": {"message": "Invalid token"}}))
                    await websocket.close()
                    break

            elif not token_validated:
                await websocket.send(json.dumps({"type": "ERROR", "payload": {"message": "Unauthorized"}}))
                await websocket.close()
                break

            elif msg_type == "SUBSCRIBE":
                device_id = payload.get("device_id")
                if device_id:
                    connected_admins.add(websocket)
                    device_subscriptions.setdefault(device_id, set()).add(websocket)

            elif msg_type == "TELEMETRY":
                device_id = payload.get("device_id")
                if not device_id:
                    continue
                # Отправляем всем подписанным
                for admin in device_subscriptions.get(device_id, []):
                    try:
                        await admin.send(json.dumps(data))
                    except:
                        pass  # соединение могло быть закрыто
    finally:
        connected_admins.discard(websocket)
        for subs in device_subscriptions.values():
            subs.discard(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Бесконечное ожидание

asyncio.run(main())
