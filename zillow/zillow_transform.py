import pandas as pd 
import numpy as np
from datetime import datetime

class ZillowTransform:
    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 

    def convert_time(self, unix: any):
        """Convert time from unix to utc"""
        if pd.isnull(unix) == True:
            return unix
        
        date = datetime.fromtimestamp(unix).strftime('%Y-%m-%d')
        return date

    def clean_zillow_data(self, data: list[any]) -> pd.DataFrame: 
        """Clean the dataframe """

        df = pd.DataFrame(data)

        df['house_id'] = df['house_id'].astype(int)
        df['date_price_change'] = df['date_price_change'] / 1000
        df['date_price_change'] = df['date_price_change'].apply(self.convert_time)
        df['date_extracted'] = self.date

        return df 
    
    def compute_analytics(self, data: pd.DataFrame, city: str) -> pd.DataFrame: 
        "Compute the median home price for a city"
        df = pd.DataFrame(data['price'])
        print("data head: ", data.head())

        df['median_price'] = np.median(data['price'])
        df['city'] = city 
        df['date_extracted'] = self.date
        df = df.drop(columns='price')

        print("df head: ", df.head())

        return df 
    