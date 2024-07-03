import streamlit as st
import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()  # Lädt Umgebungsvariablen aus .env Datei

server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
driver= '{ODBC Driver 17 for SQL Server}'

def get_data():
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        query = "SELECT * FROM SensorData"
        df = pd.read_sql(query, conn)
    return df

st.title('Wetterstation Dashboard')
data = get_data()
st.line_chart(data['SensorValue'])
