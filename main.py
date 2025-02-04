import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict
import json
import random  # Simulating ML model processing


# Define the app
app = FastAPI()

# In-memory data storage and websocket connections
data_store: List[Dict] = []  # Stores the data that is posted via the POST endpoint
connected_websockets: List[WebSocket] = []  # List of connected websocket clients
ml_response = {}
input_data = {}


# Define a Pydantic model for the data to be posted
class Data(BaseModel):
    message: str  # Replace with your actual data model

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# POST endpoint to receive the data
@app.post("/post_data")
async def post_data(data: Data):
    global ml_response

    # Send the data to the connected websockets
    for websocket in connected_websockets:
        await websocket.send_json({"type": "input_data", "message": data.message})

    # Now await until ml_response is available
    while True:
        if "data" in ml_response:
            break
        await asyncio.sleep(1)
    
    response = ml_response
    ml_response = {}

    return {"status": "success", "data": response}


# WebSocket endpoint to subscribe to the data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global ml_response
    await websocket.accept()
    connected_websockets.append(websocket)
    try:
        while True:
            # Wait for a message from the websocket client
            # This can be a heartbeat or any specific message if needed
            data = await websocket.receive_text()

            # Check the type of message received
            # If it's ml_response, store the response
            message = json.loads(data)
            if message.get("type") == "ml_response":
                ml_response["data"] = message["data"]

    except WebSocketDisconnect:
        # Handle WebSocket disconnection
        connected_websockets.remove(websocket)


# You can include other helper functions or machine learning logic to process data here
