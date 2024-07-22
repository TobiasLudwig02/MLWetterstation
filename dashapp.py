import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pyodbc
import pandas as pd
import joblib

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

# Load prediction models
model_tomorrow_path = 'models/xgb_tomorrow_model.pkl'
model_rain_path = 'models/xgb_rain_model.pkl'

xgb_model_tomorrow = joblib.load(model_tomorrow_path)
xgb_model_rain = joblib.load(model_rain_path)

# Define the mappings
weather_mapping = {
    0: 'Nice weather (sunny)',
    1: 'Regular weather',
    2: 'Bad weather (raniy or stormy)'
}

rain_mapping = {
    0: 'No',
    1: 'Yes'
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Helper function to create KPI cards
def create_kpi_card(title, id):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className='card-title'),
            html.H3(id=id, className='card-text'),
        ], className='kpi-card-body'),
        className='mb-4 kpi-card'
    )

# Create the layout of the dashboard
app.layout = dbc.Container([
    html.Div(id='main-container', children=[
        html.H1("Weather Dashboard", className='mb-4 mt-4 title-black'),
        dbc.Row([
            dbc.Col(create_kpi_card("Current Temperature", 'current-temperature'), width=3),
            dbc.Col(create_kpi_card("Current Humidity", 'current-humidity'), width=3),
            dbc.Col(create_kpi_card("Current Light Resistance", 'current-light'), width=3),
            dbc.Col(html.Img(id='weather-image', style={'width': '100%', 'max-width': '200px'}), width=3),
        ], className='mb-4 dash-container'),
        dbc.Row([
            dbc.Col(create_kpi_card("Is it raining right now?", 'prediction-rain'), width=3),
            dbc.Col(create_kpi_card("Weather forecast", 'prediction-tomorrow'), width=3),
        ], className='mb-4 dash-container'),
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['Timestamp'].min(),
                end_date=df['Timestamp'].max(),
                display_format='YYYY-MM-DD',
                className='mb-4'
            ), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='temperature-graph'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='humidity-graph'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='light-graph'), width=12),
        ])
    ])
], fluid=True, id='main-background')

# Update KPIs and image
@app.callback(
    [Output('current-temperature', 'children'),
     Output('current-humidity', 'children'),
     Output('current-light', 'children'),
     Output('weather-image', 'src'),
     Output('main-background', 'className'),
     Output('prediction-tomorrow', 'children'),
     Output('prediction-rain', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_kpis(start_date, end_date):
    filtered_df = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
    latest_record = filtered_df.iloc[-1]
    
    # Determine weather condition based on light resistance
    if latest_record['Light'] > 1000:  # assuming higher resistance means sunny weather
        weather_image = '/assets/sonnig.png'
        bg_class = 'sunny-bg'
    else:
        weather_image = '/assets/bewoelkt.png'
        bg_class = 'cloudy-bg'
    
    # Prepare data for predictions
    today_df = filtered_df[filtered_df['Timestamp'].dt.date == pd.Timestamp.today().date()]
    if not today_df.empty:
        avg_temp = today_df['Temperature'].mean()
        avg_humidity = today_df['Humidity'].mean()
        
        df_tomorrow = pd.DataFrame({"Temperature (C)": [avg_temp], "Humidity": [avg_humidity]})
        prediction_tomorrow = xgb_model_tomorrow.predict(df_tomorrow)
        weather_description = weather_mapping.get(prediction_tomorrow[0], 'unbekannter Wert')
        
        df_rain = pd.DataFrame({"Temperature (C)": [avg_temp], "Humidity": [avg_humidity]})
        prediction_rain = xgb_model_rain.predict(df_rain)
        rain_description = rain_mapping.get(prediction_rain[0], 'unbekannter Wert')
    else:
        weather_description = "Keine Daten für heute verfügbar"
        rain_description = "Keine Daten für heute verfügbar"
    
    return (
        f"{latest_record['Temperature']} °C", 
        f"{latest_record['Humidity']} %", 
        f"{latest_record['Light']} Ω", 
        weather_image,
        bg_class,
        f"{weather_description}",
        f"{rain_description}"
    )

# Update Graphs
@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('light-graph', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(start_date, end_date):
    filtered_df = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
    temp_fig = px.line(filtered_df, x='Timestamp', y='Temperature', title='Temperature Over Time')
    humidity_fig = px.line(filtered_df, x='Timestamp', y='Humidity', title='Humidity Over Time')
    light_fig = px.line(filtered_df, x='Timestamp', y='Light', title='Light Resistance Over Time')
    return temp_fig, humidity_fig, light_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
