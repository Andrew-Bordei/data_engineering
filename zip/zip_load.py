import mysql.connector
import pandas as pd 
import json 
from datetime import datetime
from config import CONFIG

class ZipLoad:
    def __init__(self):
        self.database = mysql.connector.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG['database']
        )

    def load_json(self, data: dict[str, any], city: str):
        date = datetime.today().strftime('%Y-%m-%d')

        with open(f'zip_data_{city}_{date}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return print('Data was successfully saved!')

    def load_clean_data(self, df: pd.DataFrame, table_name: str) -> int:   
        """Insert cleaned data into a MySQL table """ 
        cursor = self.database.cursor()

        # Convert dataframe to a tuple to comply with executemany requirements 
        data = [tuple(x) for x in df.to_numpy()]

        sql_statement = f"""
            INSERT INTO {table_name}
            (salary, count, city, date_extracted)
            VALUES (%s, %s, %s, %s);
        """

        cursor.executemany(sql_statement, data)
        self.database.commit()

        return print(f'Clean data was successfully inserted into {table_name}!')
    
    def load_analytics(self, data: list[any], table_name: str) -> str: 
        """Insert analytics into table"""
        cursor = self.database.cursor()

        tuple_data = tuple(data)

        sql_statement = f"""
            INSERT INTO {table_name}
            (median_salary, city, date_extracted)
            VALUES (%s, %s, %s);
        """

        cursor.execute(sql_statement, tuple_data)
        self.database.commit()

        return print(f'Analytics data was successfully inserted into {table_name}!')
    
    def close_database_connection(self):
        pass
        # my_cursor.close()
        # self.database.close()