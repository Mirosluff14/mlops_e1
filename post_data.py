import requests

# post some data to /post_data endpoint

data = {"message": {"Your input data, can be in any format you need": ["x1", "x2"], "foo":"bar"}, "type": "input_data"} 
print("Posting data:", data)
response = requests.post("https://mlops-e1-fastapi.onrender.com/post_data", json=data)
print(response.json())