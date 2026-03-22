from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active = {}

    async def connect(self, match_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(match_id, []).append(websocket)

    def disconnect(self, match_id: int, websocket: WebSocket):
        self.active[match_id].remove(websocket)

    async def broadcast(self, match_id: int, message: dict):
        for ws in self.active.get(match_id, []):
            await ws.send_json(message)
