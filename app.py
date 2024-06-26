import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os

# Laden der Umgebungsvariablen aus der .env Datei
load_dotenv()

# PostgreSQL-Verbindungszeichenfolge aus der Umgebungsvariable
conn_str = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')

# Konvertieren der Verbindungszeichenfolge in ein URL-Objekt für SQLAlchemy
conn_url = URL.create(
    drivername='postgresql+psycopg2',
    database=None,  # database is already included in the connection string
    query=dict(
        dbname=conn_str.split(' ')[0].split('=')[1],
        host=conn_str.split(' ')[1].split('=')[1],
        port=conn_str.split(' ')[2].split('=')[1],
        sslmode=conn_str.split(' ')[3].split('=')[1],
        user=conn_str.split(' ')[4].split('=')[1],
        password=conn_str.split(' ')[5].split('=')[1],
    )
)

# Verbindung zur Azure PostgreSQL-Datenbank herstellen
engine = create_engine(conn_url)

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
