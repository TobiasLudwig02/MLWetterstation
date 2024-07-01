import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os
import psycopg2

# Laden der Umgebungsvariablen aus der .env Datei
load_dotenv()

# PostgreSQL-Verbindungszeichenfolge aus der Umgebungsvariable
conn_str = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')

# Funktion zum Parsen der Verbindungszeichenfolge und Extrahieren der Parameter
def parse_connection_string(conn_str):
    params = {}
    for param in conn_str.split():
        key, value = param.split('=')
        params[key] = value
    return params

# Extrahieren der Verbindungsparameter
params = parse_connection_string(conn_str)

# Streamlit App
st.set_page_config(page_title="Wetterstation", page_icon=":sun_behind_rain_cloud:", layout="wide")

st.title("🌤️ Wetterstation Dashboard")

# Funktion zum Testen der Datenbankverbindung
def check_db_connection():
    try:
        # Verbindung zur Datenbank herstellen
        connection = psycopg2.connect(
            user=params['user'], 
            password=params['password'], 
            host=params['host'], 
            port=params['port'], 
            database=params['dbname'],
            sslmode=params['sslmode']
        )
        # Testabfrage
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Fehler bei der Verbindung zur Datenbank: {e}")
        return False

# Verbindung testen
if check_db_connection():
    st.success("Verbindung zur Datenbank erfolgreich!")
else:
    st.error("Verbindung zur Datenbank fehlgeschlagen.")
