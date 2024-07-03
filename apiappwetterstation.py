from flask import Flask, request, jsonify
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()  # Lädt Umgebungsvariablen aus .env Datei

app = Flask(__name__)

server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
driver= '{ODBC Driver 17 for SQL Server}'

@app.route('/api/sensor-data', methods=['POST'])
def sensor_data():
    sensor_data = request.get_json()
    sensor_value = sensor_data.get('sensorValue')

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO SensorData (SensorValue) VALUES (?)", sensor_value)

    return jsonify({'status': 'success', 'data': sensor_data})

if __name__ == '__main__':
    app.run(debug=True)
