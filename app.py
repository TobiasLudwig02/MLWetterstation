import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import urllib
from dotenv import load_dotenv
import os

# Laden der Umgebungsvariablen aus der .env Datei
load_dotenv()

# Azure SQL-Datenbankverbindungsinformationen aus Umgebungsvariablen
server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Verbindungszeichenfolge für SQLAlchemy
connection_string = f"mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)

# Verbindung zur temporären SQLite-Datenbank herstellen
engine = create_engine('sqlite:///weather_data.db')

# Funktion zum Generieren zufälliger Wetterdaten
def generate_random_data(num_records=100):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=num_records).tolist()
    temperature = np.random.uniform(low=-10, high=35, size=num_records).tolist()
    humidity = np.random.uniform(low=20, high=100, size=num_records).tolist()
    wind_speed = np.random.uniform(low=0, high=15, size=num_records).tolist()

    data = {
        'date': dates,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed
    }

    df = pd.DataFrame(data)
    return df

# Daten generieren und in die Datenbank schreiben
def create_and_populate_db():
    df = generate_random_data()
    with engine.connect() as connection:
        df.to_sql('weather_data', connection, if_exists='replace', index=False)

# Wetterdaten abrufen
def get_weather_data():
    query = "SELECT * FROM weather_data"
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

# Streamlit App
st.set_page_config(page_title="Wetterstation", page_icon=":sun_behind_rain_cloud:", layout="wide")

st.title("🌤️ Wetterstation Dashboard")

# Temporäre Datenbank erstellen und befüllen
create_and_populate_db()

# Daten abrufen
data = get_weather_data()

# Letzten Datensatz anzeigen
latest_data = data.iloc[-1]
st.metric(label="Temperatur", value=f"{latest_data['temperature']:.1f} °C")
st.metric(label="Luftfeuchtigkeit", value=f"{latest_data['humidity']:.1f} %")
st.metric(label="Windgeschwindigkeit", value=f"{latest_data['wind_speed']:.1f} km/h")

# Daten in einer Tabelle anzeigen
st.subheader("Letzte Wetterdaten")
st.dataframe(data)

# Liniencharts für Temperatur und Luftfeuchtigkeit
st.subheader("Temperaturverlauf")
st.line_chart(data['temperature'])

st.subheader("Luftfeuchtigkeitsverlauf")
st.line_chart(data['humidity'])

# Optional: Stil verbessern
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
    .stMetric {
        font-size: 2em;
    }
</style>
""", unsafe_allow_html=True)
