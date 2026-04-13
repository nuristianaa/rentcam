from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        # Struktur: { topic: { user_id: [ws1, ws2] } }
        self.connections: dict[str, dict[int | str, set[WebSocket]]] = {}

    async def connect(self, user_id: int | str, websocket: WebSocket, topic: str):
        await websocket.accept()
        if topic not in self.connections:
            self.connections[topic] = {}
        if user_id not in self.connections[topic]:
            self.connections[topic][user_id] = set()
        
        self.connections[topic][user_id].add(websocket)

    def disconnect(self, user_id: int | str, topic: str, websocket: WebSocket):
        if topic in self.connections and user_id in self.connections[topic]:
            self.connections[topic][user_id].discard(websocket)
            # Bersihkan jika tidak ada koneksi lagi
            if not self.connections[topic][user_id]:
                del self.connections[topic][user_id]
            if not self.connections[topic]:
                del self.connections[topic]

    async def push(self, topic: str, user_id: int | str, message: dict):
        print('masuk ws 1', topic, user_id)
        if topic in self.connections and user_id in self.connections[topic]:
            # Kirim ke semua tab/stack yang dimiliki user tersebut
            live_connections = self.connections[topic][user_id]
            for ws in list(live_connections):
                try:
                    await ws.send_json(message)
                except Exception:
                    live_connections.remove(ws)

manager = WebSocketManager()