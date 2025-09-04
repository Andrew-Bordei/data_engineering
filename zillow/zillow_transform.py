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
    
    def compute_analytics(self, df: pd.DataFrame, city: str) -> list[any]: 
        "Compute the median home price for a city"
        data = []

        data.append(np.median(df['price']))
        data.append(city) 
        data.append(self.date)

        return data 
    