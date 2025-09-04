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

    zillow_statement = f"""
        SELECT date_extracted, median_price
        FROM zillow_analytics
        WHERE city LIKE %s; 
    """

    zip_statement = f"""
        SELECT date_extracted, median_salary
        FROM zip_analytics
        WHERE city LIKE %s;
    """

    params = (f"%{city}%",)

    my_cursor.execute(zillow_statement, params)
    zillow_data = my_cursor.fetchall()
    zillow_df = pd.DataFrame(zillow_data, columns=['date_extracted', 'median_price'])

    my_cursor.execute(zip_statement, params)
    zip_data = my_cursor.fetchall()
    zip_df = pd.DataFrame(zip_data, columns=['date_extracted', 'median_salary'])

    return [zillow_df, zip_df]

def price_income(zillow_df: pd.DataFrame, zip_df: pd.DataFrame):
    """Calculate the price to income for given city"""
    ratio = zillow_df['median_price'] / zip_df['median_salary']

    ratio_df = pd.DataFrame(ratio, columns=['price_income_ratio'])
    ratio_df['date_extracted'] = zillow_df['date_extracted']

    return ratio_df

def display_chart(df: pd.DataFrame, city: str) -> px.line:
    """Plot a line chart with data"""
    fig = px.line(df, x='date_extracted', y='price_income_ratio', title=f"Price to Income Ratio in {city}")
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
    dataframes = extract_data(city)
    analytics = price_income(dataframes[0], dataframes[1])
    fig = display_chart(analytics, city)
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
