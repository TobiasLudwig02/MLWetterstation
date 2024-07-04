from flask import Flask, request
import pyodbc

app = Flask(__name__)

# Datenbankverbindung
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=wetterstation.database.windows.net;'
    'DATABASE=wetterstation;'
    'UID=dhbw;'
    'PWD=Wetterstation1.'
)

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json
    temperature = data['temperature']
    humidity = data['humidity']

    cursor = conn.cursor()
    cursor.execute("INSERT INTO SensorData (Temperature, Humidity) VALUES (?, ?)", temperature, humidity)
    conn.commit()
    return 'Data received and stored', 200

if __name__ == '__main__':
    app.run(debug=True)