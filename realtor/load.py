import mysql.connector
import pandas as pd 
from datetime import datetime
from config.config import CONFIG

class Load:
    def __init__(self):
        self.database = mysql.connector.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG['database']
        )
        self.date = datetime.today().strftime('%Y-%m-%d') 
    
    def load_database(self, df: pd.DataFrame, table_name: str) -> int:   
        """Insert cleaned data into a MySQL table""" 
        my_cursor = self.database.cursor()

        # Convert df to tuple & change nan -> None to comply with mysql reqs 
        data = [tuple(None if pd.isna(x) else x for x in row)
            for row in df.itertuples(index=False, name=None)]

        sql_statement = f"""
            INSERT INTO {table_name} 
            (property_id, list_price, listing_id, beds, baths, sqft,             
            lot_sqft, year_built, garage_num, address_line, postal_code, state_code,       
            city, advertiser_name, advertiser_office, last_price_change_amount, date_acquired)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        my_cursor.executemany(sql_statement, data)
        self.database.commit()
        # my_cursor.close()
        # self.database.close()
        return print(f'Clean data successfully inserted into {table_name}!')

    def load_csv(self, df: pd.DataFrame) -> str: 
        df.to_csv(f"realtor_data_{self.date}.csv")
        return print("Data was saved to csv!")
    
    def controller(self, load_method: str, df: pd.DataFrame) -> str: 
        if load_method == 'database': 
            result = self.load_database(df, 'realtor_data')
        elif load_method == 'csv':
            result = self.load_csv(df)
        return result

        