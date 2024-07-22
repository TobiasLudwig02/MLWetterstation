import requests

url = "http://apiappwetterstation.azurewebsites.net/send_data"
data = {
    "temperature": 100,
    "humidity": 68,
    "light": 32
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.text)
