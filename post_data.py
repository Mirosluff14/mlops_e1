import requests

# post some data to /post_data endpoint

data = {"message": "Hello, World!", "type": "input_data"} 
print("Posting data:", data)
response = requests.post("http://localhost:8000/post_data", json=data)
print(response.json())