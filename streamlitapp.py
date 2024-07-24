import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
import joblib
from datetime import timedelta
import datetime as dt

# Set page configuration to use full width
st.set_page_config(layout="wide")

# Database connection parameters
server = 'wetterstation.database.windows.net'
database = 'wetterstation'
username = 'dhbw'
password = 'Wetterstation1.'

# Create the connection string
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Connect to the database and fetch the data
conn = pyodbc.connect(conn_str)
query = "SELECT * FROM Weatherdata WHERE Timestamp >= '2024-07-19T00:00:00'"
df = pd.read_sql(query, conn)
conn.close()

# Add 2h for timedifference
df['Timestamp'] = pd.to_datetime(df['Timestamp']) + timedelta(hours=2)

# Load prediction models
model_tomorrow_path = 'assets/xgb_tomorrow_model.pkl'
model_rain_path = 'assets/xgb_rain_model.pkl'

xgb_model_tomorrow = joblib.load(model_tomorrow_path)
xgb_model_rain = joblib.load(model_rain_path)

# Define the mappings
weather_mapping = {
    0: 'Nice weather (sunny)',
    1: 'Regular weather',
    2: 'Bad weather (rainy or stormy)'
}

rain_mapping = {
    0: 'No',
    1: 'Yes'
}

# Streamlit app
st.title("Weather Dashboard")

# Date range selection
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start date", value=dt.date(2024, 7, 19))
with col2:
    end_date = st.date_input("End date", value=dt.date(2024, 7, 26))

filtered_df = df[(df['Timestamp'] >= pd.to_datetime(start_date)) & (df['Timestamp'] <= pd.to_datetime(end_date))]
latest_record = filtered_df.iloc[-1]

# Display current values in columns
col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric("Current Temperature", f"{latest_record['Temperature']} °C")
with col4:
    st.metric("Current Humidity", f"{latest_record['Humidity']} %")
with col5:
    st.metric("Current Light Resistance", f"{latest_record['Light']} Ω")
with col6:
    # Determine weather condition based on light resistance
    if latest_record['Light'] > 1000:
        weather_image = 'assets/sonnig_hell.png'

        st.image(weather_image, width=200)
    else:
        weather_image = 'assets/bewoelkt_hell.png'
        st.image(weather_image, width=200)


# Prepare data for predictions
today_df = filtered_df[filtered_df['Timestamp'].dt.date == pd.Timestamp.today().date()]
if not today_df.empty:
    avg_temp = today_df['Temperature'].mean()
    avg_humidity = today_df['Humidity'].mean()

    df_tomorrow = pd.DataFrame({"Temperature (C)": [avg_temp], "Humidity": [avg_humidity]})
    prediction_tomorrow = xgb_model_tomorrow.predict(df_tomorrow)
    weather_description = weather_mapping.get(prediction_tomorrow[0], 'NaN')

    df_rain = pd.DataFrame({"Temperature (C)": [avg_temp], "Humidity": [avg_humidity]})
    prediction_rain = xgb_model_rain.predict(df_rain)
    rain_description = rain_mapping.get(prediction_rain[0], 'NaN')
else:
    weather_description = "NaN"
    rain_description = "NaN"

# Display predictions below KPIs
col7, col8 = st.columns(2)

with col7:
    st.metric("Weather forecast", weather_description)
with col8:
    st.metric("Is it raining right now?", rain_description)

# Plot graphs
temp_fig = px.line(filtered_df, x='Timestamp', y='Temperature', title='Temperature Over Time')
humidity_fig = px.line(filtered_df, x='Timestamp', y='Humidity', title='Humidity Over Time')
light_fig = px.line(filtered_df, x='Timestamp', y='Light', title='Light Resistance Over Time')

st.plotly_chart(temp_fig, use_container_width=True)
st.plotly_chart(humidity_fig, use_container_width=True)
st.plotly_chart(light_fig, use_container_width=True)

