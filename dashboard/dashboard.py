import pandas as pd
import mysql.connector
import plotly.express as px 
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

from config import CONFIG

def extract_data(city: str) -> pd.DataFrame: 
    """Query the SQL db to get city data"""
    database = mysql.connector.connect(
        host=CONFIG['host'],
        user=CONFIG['user'],
        password=CONFIG['password'],
        database=CONFIG['database']
    )
    my_cursor = database.cursor()

    sql_statement = f"""
        SELECT date_extracted, ROUND(AVG(price), 0)
        FROM zillow_data
        WHERE address LIKE %s
        GROUP BY date_extracted
        ORDER BY date_extracted; 
    """
    params = (f"%{city}%",)

    my_cursor.execute(sql_statement, params)
    data = my_cursor.fetchall()
    df = pd.DataFrame(data, columns=['date_extracted', 'avg_price'])

    return df

def display_chart(df: pd.DataFrame, city: str) -> px.line:
    """Plot a line chart with data"""
    fig = px.line(df, x='date_extracted', y='avg_price', title=f"Average Home Price in {city}")
    fig.update_traces(mode="lines+markers")
    return fig

app = Dash()

cities = ["Boise", "Harrisburg", "Grand Rapids"]

app.layout = [
    html.H1(children='Housing Affordability', style={'textAlign':'center'}),
    dcc.Dropdown(
        cities, 
        id='dropdown-selection', 
        value='City',
        ),
    dcc.Graph(
        id='graph-content',
        config={"responsive": True}, 
        style={"width": "100%", "height": "60vh"}
    )
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(city):
    df = extract_data(city)
    fig = display_chart(df, city)
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
