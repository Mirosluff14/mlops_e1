# This here is an emulation of how your local machine learning model can respond to input data in real-time to serve the response from api.

import asyncio
import websockets
import json

async def listen_to_data():
    # URL of your FastAPI WebSocket endpoint
    uri = "wss://mlops-e1-fastapi.onrender.com/ws"  # Replace with your server's URL (NOTE: wss is secure version of ws, Render comes with SSL)

    # Connect to the WebSocket
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")

        # Keep listening for incoming messages from the WebSocket
        while True:
            # Receive a message from the WebSocket server
            response = await websocket.recv()
            response_data = json.loads(response)
            print(response_data.get("type"))
            print(response_data)

            # Check if the received message contains new data
            if response_data.get("type") == "input_data":
                print("Received new data:", response_data["message"])

                # Here you can process the data (e.g., run machine learning algorithms)
                # In this case, we're just simulating the processing by sending a response
                processed_data = "Processed data based on: " + str(response_data["message"])

                # Send the response back to the server after processing
                await websocket.send(json.dumps({"type": "ml_response", "data": processed_data}))
                print("Sent response:", processed_data)

# Run the WebSocket listener in an event loop
asyncio.get_event_loop().run_until_complete(listen_to_data())
