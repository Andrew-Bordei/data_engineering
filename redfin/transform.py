import pandas as pd 
from datetime import datetime

class Transform: 
    def __init__(self)-> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 
        
    def convert_time(self, ms: int) -> float: 
        """Convert ms to days"""
        days = ms / 86400000
        return days 
    
    def convert_sqft_acres(self, sqft: int) -> float: 
        acres = sqft / 43560
        return acres 
        
    def transform(self, data: dict[str, any]) -> pd.DataFrame: 
        df = pd.DataFrame(data)

        df['time_since_listed'] = df['time_since_listed'].apply(self.convert_time)
        df['beds'] = df['beds'].astype(float)
        df['lot_size'] = df['lot_size'].apply(self.convert_sqft_acres)
        df['year_built'] = df['year_built'].fillna(0).astype(int)
        df['date_acquired'] = self.date
        return df 
    
