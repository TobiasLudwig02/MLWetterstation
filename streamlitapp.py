import streamlit as st
import pyodbc
import pandas as pd

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
st.title("Sensor Data Dashboard")
data = fetch_data()
st.write(data)
