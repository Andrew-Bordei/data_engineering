import mysql.connector
import pandas as pd 

class ZillowLoad:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="!?65DataToTradr&/93",
            database="economy"
        )
    
    def load_zillow_data(self, df: pd.DataFrame, table_name: str) -> int:   
        """Insert cleaned data into a MySQL table""" 
        my_cursor = self.database.cursor()

        # Convert dataframe to a tuple to comply with executemany requirements 
        # data = [tuple(x) for x in df.to_numpy()]

        # Convert df to tuple & change nan -> None to comply with mysql reqs 
        data = [tuple(None if pd.isna(x) else x for x in row)
            for row in df.itertuples(index=False, name=None)]

        sql_statement = f"""
            INSERT INTO {table_name} 
            (house_id, address, price, tax_assessed_price, bedrooms,
            bathrooms, living_sqft, lot_sqft, lot_unit, days_on_zillow,
            price_change, date_price_change, zestimate, rent_zestimate,
            home_status, home_type, non_owner_occupied, preforeclosure_auction,
            premier_builder, marketing_status, broker, country_currency, date_extracted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        my_cursor.executemany(sql_statement, data)

        self.database.commit()
        # my_cursor.close()
        # self.database.close()

        return print(f'Clean data was successfully inserted into {table_name}!')
        
