import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict
import json


# Define the app
app = FastAPI()

connected_websockets: List[WebSocket] = []  # List of connected websocket clients
ml_response = {}  # Store the response from the ML model

# Define a Pydantic model for the data to be posted
class Data(BaseModel):
    message: Dict  # Replace with your actual data model with dtypes (numpy array, etc.)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# POST endpoint to receive the data
@app.post("/post_data")
async def post_data(data: Data):
    global ml_response # define ml_response as global variable to access it from other functions

    # Add timer for the timeout
    timer = 0

    # Send the data to the connected websockets
    for websocket in connected_websockets:
        await websocket.send_json({"type": "input_data", "message": data.message})

    # Now await until ml_response is available
    while True:
        if "data" in ml_response:
            break
        await asyncio.sleep(1)
        timer += 1
        if timer > 10:  # Timeout after 10 seconds
            return {"status": "error", "message": "Timeout: ML model response not received"}
    
    response = ml_response
    ml_response = {} # Reset the ml_response for the next request

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
