from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from .ws_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: int = Query(...), topic: str = Query(...)):
    """
    FE connect ke topic tertentu
    ws://localhost:8000/ws?user_id=123&topic=approval
    """
    await manager.connect(user_id, websocket, topic)
    try:
        while True:
            await websocket.receive_text()  # optional, FE bisa ping
    except WebSocketDisconnect:
        manager.disconnect(user_id, topic)