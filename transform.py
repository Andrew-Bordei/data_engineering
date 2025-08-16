import pandas as pd 
from datetime import datetime

class Transform:
    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 

    def convert_time(self, unix: any):
        if pd.isnull(unix) == True:
            return unix
        
        date = datetime.fromtimestamp(unix).strftime('%Y-%m-%d')
        return date

    def clean_zillow_data(self, df: pd.DataFrame, path: str) -> pd.DataFrame: 
        """
        Clean the dataframe  
        """ 
        df['house_id'] = df['house_id'].astype(int)

        df['date_price_change'] = df['date_price_change'] / 1000

        df['date_price_change'] = df['date_price_change'].apply(self.convert_time)

        df['date_extracted'] = path[-15:-5]
        
        return df 
    