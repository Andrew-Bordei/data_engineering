import pandas as pd 
from datetime import datetime

class Transform:
    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 
    
    def transform_zip_data(self, df: pd.DataFrame, city: str) -> pd.DataFrame: 
        df['city'] = city 
        df['date_extracted'] = self.date

        return df 