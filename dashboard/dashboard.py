import pandas as pd
import mysql.connector
import plotly.express as px 
from config import CONFIG

def extract_data(city:str) -> pd.DataFrame: 
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

def display_chart(df: pd.DataFrame, city: str, state: str) -> None:
    fig = px.line(df, x='date_extracted', y='avg_price', title=f"Average Home Price in {city}, {state}")
    fig.show()

if __name__ == '__main__': 
    city = 'Grand Rapids'
    state = "MI"
    data = extract_data(city)
    display_chart(data, city, state)