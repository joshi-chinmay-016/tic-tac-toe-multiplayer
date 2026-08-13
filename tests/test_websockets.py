import pytest
from app.websocket.manager import ConnectionManager
import asyncio

class MockWebSocket:
    def __init__(self):
        self.accepted = False
        self.messages = []
        self.closed = False

    async def accept(self):
        self.accepted = True

    async def send_json(self, data):
        self.messages.append(data)

    async def close(self, code=1000):
        self.closed = True

@pytest.mark.asyncio
async def test_connection_manager_connect():
    manager = ConnectionManager()
    ws = MockWebSocket()

    await manager.connect(match_id=1, user_id=10, websocket=ws)
    assert ws.accepted == True
    assert 1 in manager.active
    assert len(manager.active[1]) == 1
    assert manager.active[1][0][0] == 10

@pytest.mark.asyncio
async def test_connection_manager_broadcast():
    manager = ConnectionManager()
    ws1 = MockWebSocket()
    ws2 = MockWebSocket()

    await manager.connect(match_id=1, user_id=10, websocket=ws1)
    await manager.connect(match_id=1, user_id=11, websocket=ws2)

    await manager.broadcast(1, {"type": "test"})
    assert len(ws1.messages) == 1
    assert len(ws2.messages) == 1
    assert ws1.messages[0]["type"] == "test"

@pytest.mark.asyncio
async def test_connection_manager_disconnect():
    manager = ConnectionManager()
    ws1 = MockWebSocket()

    await manager.connect(match_id=1, user_id=10, websocket=ws1)
    manager.disconnect(1, 10, ws1)

    assert len(manager.active[1]) == 0
    assert 10 in manager.disconnected[1]
