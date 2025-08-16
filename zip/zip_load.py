import mysql.connector
import pandas as pd 
import json 
from datetime import datetime

class ZipLoad:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="!?65DataToTradr&/93",
            database="economy"
        )

    def load_json(self, data: dict[str, any], city: str):
        date = datetime.today().strftime('%Y-%m-%d')

        with open(f'zip_data_{city}_{date}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

        return print('Data was successfully saved!')
    

    def load_database(self, df: pd.DataFrame, table_name: str) -> int:   
        """
        Insert cleaned data into a MySQL database 
        """ 
        my_cursor = self.database.cursor()

        # Convert dataframe to a tuple to comply with executemany requirements 
        data = [tuple(x) for x in df.to_numpy()]

        sql_statement = f"""
            INSERT INTO {table_name}
            (salary, count, city, date_extracted)
            VALUES (%s, %s, %s, %s);
        """

        my_cursor.executemany(sql_statement, data)

        self.database.commit()
        # my_cursor.close()
        # self.database.close()

        return print(f'Clean data was successfully inserted into {table_name}!')