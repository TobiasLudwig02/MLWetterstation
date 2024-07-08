import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

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
    return df

# Streamlit-Anwendung
st.title("Wetterstation Dashboard")

# Daten laden
data = fetch_data()

# Metriken
col1, col2, col3 = st.columns(3)
col1.metric("Durchschnittstemperatur (°C)", round(data['Temperature'].mean(), 2))
col2.metric("Durchschnittliche Luftfeuchtigkeit (%)", round(data['Humidity'].mean(), 2))
col3.metric("Durchschnittliche Lichtintensität (Lux)", round(data['Light'].mean(), 2))

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
ax.set_ylabel('Lichtintensität (Lux)')
ax.legend()
st.pyplot(fig)

# Alle Diagramme nebeneinander anzeigen
st.subheader("Alle Werte gleichzeitig")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
fig.tight_layout(pad=5.0)

# Temperatur
ax1.plot(data['Timestamp'], data['Temperature'], label='Temperatur', color='red')
ax1.set_xlabel('Zeit')
ax1.set_ylabel('Temperatur (°C)')
ax1.legend()

# Luftfeuchtigkeit
ax2.plot(data['Timestamp'], data['Humidity'], label='Luftfeuchtigkeit', color='blue')
ax2.set_xlabel('Zeit')
ax2.set_ylabel('Luftfeuchtigkeit (%)')
ax2.legend()

# Lichtintensität
ax3.plot(data['Timestamp'], data['Light'], label='Lichtintensität', color='green')
ax3.set_xlabel('Zeit')
ax3.set_ylabel('Lichtintensität (Lux)')
ax3.legend()

st.pyplot(fig)