import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Datenbankverbindung
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=wetterstation.database.windows.net;'
    'DATABASE=wetterstation;'
    'UID=dhbw;'
    'PWD=Wetterstation1.'
)

# Daten abfragen
def fetch_data():
    query = "SELECT * FROM Weatherdata"
    df = pd.read_sql(query, conn)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

# Streamlit-Anwendung
st.title("Wetterstation Dashboard")

# Daten laden
data = fetch_data()

# Filter für die letzten 5 Minuten
now = datetime.now()
last_5_minutes = now - timedelta(minutes=5)
data_last_5_minutes = data[data['Timestamp'] >= last_5_minutes]

st.subheader("Durchschnitt der Metriken der letzten 5 Minuten")

# Metriken
col1, col2, col3 = st.columns(3)
col1.metric("Durchschnittstemperatur (°C)", round(data_last_5_minutes['Temperature'].mean(), 2))
col2.metric("Durchschnittliche Luftfeuchtigkeit (%)", round(data_last_5_minutes['Humidity'].mean(), 2))
col3.metric("Durchschnittliche Lichtintensität (Ohm)", round(data_last_5_minutes['Light'].mean(), 2))


# Temperatur über die Zeit
st.subheader("Temperatur über die Zeit")
fig, ax = plt.subplots()
ax.plot(data['Timestamp'], data['Temperature'], label='Temperatur', color='red')
ax.set_xlabel('Zeit')
ax.set_ylabel('Temperatur (°C)')
ax.legend()
st.pyplot(fig)

# Luftfeuchtigkeit über die Zeit
st.subheader("Luftfeuchtigkeit über die Zeit")
fig, ax = plt.subplots()
ax.plot(data['Timestamp'], data['Humidity'], label='Luftfeuchtigkeit', color='blue')
ax.set_xlabel('Zeit')
ax.set_ylabel('Luftfeuchtigkeit (%)')
ax.legend()
st.pyplot(fig)

# Lichtintensität über die Zeit
st.subheader("Lichtintensität über die Zeit")
fig, ax = plt.subplots()
ax.plot(data['Timestamp'], data['Light'], label='Lichtintensität', color='green')
ax.set_xlabel('Zeit')
ax.set_ylabel('Lichtintensität (Ohm)')
ax.legend()
st.pyplot(fig)

# Alle Werte gleichzeitig anzeigen
st.subheader("Alle Werte gleichzeitig")

fig, ax1 = plt.subplots(figsize=(10, 6))

# Temperatur und Luftfeuchtigkeit
ax1.plot(data['Timestamp'], data['Temperature'], label='Temperatur (°C)', color='red')
ax1.plot(data['Timestamp'], data['Humidity'], label='Luftfeuchtigkeit (%)', color='blue')
ax1.set_xlabel('Zeit')
ax1.set_ylabel('Temperatur (°C) und Luftfeuchtigkeit (%)')
ax1.legend(loc='upper left')

# Zweite y-Achse für Lichtintensität
ax2 = ax1.twinx()
ax2.plot(data['Timestamp'], data['Light'], label='Lichtintensität (Ohm)', color='green')
ax2.set_ylabel('Lichtintensität (Ohm)')
ax2.legend(loc='upper right')

st.pyplot(fig)