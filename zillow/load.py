import mysql.connector
import pandas as pd 
from config import CONFIG

class Load:
    def __init__(self):
         self.database = mysql.connector.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG['database']
        )
    
    def load_data(self, df: pd.DataFrame, table_name: str) -> int:   
        """Insert cleaned data into a MySQL table""" 
        my_cursor = self.database.cursor()

        # Convert df to tuple & change nan -> None to comply with mysql reqs 
        data = [tuple(None if pd.isna(x) else x for x in row)
            for row in df.itertuples(index=False, name=None)]

        sql_statement = f"""
            INSERT INTO {table_name} 
            (house_id, address, price, tax_assessed_price, bedrooms,
            bathrooms, living_sqft, lot_sqft, lot_unit, days_on_zillow,
            price_change, date_price_change, zestimate, rent_zestimate,
            home_status, home_type, non_owner_occupied, preforeclosure_auction,
            premier_builder, marketing_status, broker, country_currency, date_extracted, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        my_cursor.executemany(sql_statement, data)
        self.database.commit()
        # my_cursor.close()
        # self.database.close()

        return print(f'Clean data successfully inserted into {table_name}!')
    
    def load_analytics(self, df: pd.DataFrame, table_name: str) -> int:   
        """Insert zillow analytics into a MySQL table""" 
        my_cursor = self.database.cursor()

        data = [tuple(None if pd.isna(x) else x for x in row)
            for row in df.itertuples(index=False, name=None)]

        sql_statement = f"""
            INSERT INTO {table_name} 
            (num_active_listings, median_house_price, pct_reduced_houses, 
            mean_price_reduced, city, date_extracted)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        my_cursor.executemany(sql_statement, data)
        self.database.commit()

        return print(f'Analytics were successfully inserted into {table_name}!')

        
