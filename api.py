import requests

url = "https://twf-task-api.onrender.com/min-cost"

data = {"A": 1, "G": 1, "H": 1, "I":3} #A-1, G-1, H-1, I-3

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Request failed:", str(e))