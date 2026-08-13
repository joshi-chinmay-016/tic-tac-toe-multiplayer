from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
import time

class ConnectionManager:
    def __init__(self):
        self.active: Dict[int, List[tuple]] = {}
        self.disconnected: Dict[int, Dict[int, float]] = {}

    async def connect(self, match_id: int, user_id: int, websocket: WebSocket, is_spectator: bool = False):
        await websocket.accept()
        if match_id not in self.active:
            self.active[match_id] = []
            self.disconnected[match_id] = {}

        self.active[match_id] = [(uid, ws, spec) for (uid, ws, spec) in self.active[match_id] if uid != user_id]

        self.active[match_id].append((user_id, websocket, is_spectator))
        if user_id in self.disconnected[match_id]:
            del self.disconnected[match_id][user_id]

    def disconnect(self, match_id: int, user_id: int, websocket: WebSocket):
        if match_id in self.active:
            self.active[match_id] = [(uid, ws, spec) for (uid, ws, spec) in self.active[match_id] if ws != websocket]
            self.disconnected[match_id][user_id] = time.time()

    async def broadcast(self, match_id: int, message: dict):
        if match_id in self.active:
            for uid, ws, spec in self.active[match_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass

    async def send_personal_message(self, message: dict, match_id: int, user_id: int):
        if match_id in self.active:
            for uid, ws, spec in self.active[match_id]:
                if uid == user_id:
                    try:
                        await ws.send_json(message)
                    except Exception:
                        pass
