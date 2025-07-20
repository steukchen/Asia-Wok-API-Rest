from fastapi import APIRouter, WebSocket, WebSocketDisconnect,status,HTTPException
from typing import Dict
from app.core.security import validate_token
from datetime import datetime

active_connections: Dict[str, WebSocket] = {}

router = APIRouter()

def validate_ws_token(token:str) -> dict | None:
    try:
        data = validate_token(token=token)
    except HTTPException:
        return None
    return data

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    ws_token = await websocket.receive_text()
    data_user = validate_ws_token(ws_token)
    if not data_user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    try:
        print(active_connections.get(data_user["id"]))
        if active_connections.get(data_user["id"]):
            await active_connections[data_user["id"]].send_json(data={
                "message": "Another connection detected",
                "status": 409
            })
            await active_connections[data_user["id"]].close(reason="Another connection")
        
        active_connections[data_user["id"]] = websocket
        for c in active_connections.keys():
            print(c + ": "+str(active_connections[c]))
        while True:
            data = await websocket.receive_json()
            print(data)
            await send_action(data["message"])
            
    except WebSocketDisconnect as e:
        print(e.reason)
        if data_user:
            if (active_connections.get(data_user["id"])):
                print(data_user["id"] +" ("+data_user["rol"] +") "+str(websocket)+ " connection was closed")
                if e.reason !="Another connection":
                    del active_connections[data_user["id"]]
        else:
            print(e)

async def send_action(action: str):
    for connection in active_connections.values():
        await connection.send_json({
            "type": "action",
            "message": action,
            "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })