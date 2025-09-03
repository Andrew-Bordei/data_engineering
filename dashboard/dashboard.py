import pandas as pd
import mysql.connector
import plotly.express as px 
from config import CONFIG

database = mysql.connector.connect(
    host=CONFIG['host'],
    user=CONFIG['user'],
    password=CONFIG['password'],
    database=CONFIG['database']
)

my_cursor = database.cursor()


sql_statement = f"""
    SELECT * 
    FROM zillow_data
    WHERE date_extracted = %s 
    LIMIT 10; 
"""
params = ("2025-09-02",)

my_cursor.execute(sql_statement, params)
data = my_cursor.fetchall()
print(data)
