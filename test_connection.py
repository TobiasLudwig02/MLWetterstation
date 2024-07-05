import requests

url = "http://apiappwetterstation.azurewebsites.net/send_data"
data = {
    "temperature": 24.5,
    "humidity": 60
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.text)
