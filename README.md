# Hosting FastAPI on Render.com and connecting it to your machine for heavy computation.

This guide provides instructions on how to host the FastAPI application on Render.com.

## Steps to Host FastAPI on Render.com

1. (Optional) **Fork the Repository**: 
   - Fork this repository to your own GitHub account if you want to test this setup with your own models.

2. **Create a New Web Service on Render.com**:
   - Go to Render.com and create a new web service.
   - Connect the repository to the new web service.

3. **Build Command**:
   - Set the build command to `poetry install`.

4. **Start Command**:
   - Set the start command to `uvicorn main:app --host 0.0.0.0 --port 10000 --reload`.

5. **Run `ml_model.py` Locally**:
   - The `ml_model.py` should be run on your local machine to do the heavy computation which Render wouldn't handle. It connects to your Render service via websocket and listens for messages containing the data you send to /post_data endpoint.

6. **Testing**:
   - You can test the setup using `post_data.py`.


# WORK IN PROGRESS. If you find any bugs feel free to submit your fixes and/or contact me.
