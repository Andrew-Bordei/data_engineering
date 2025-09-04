import pandas as pd 
import numpy as np
from datetime import datetime

class ZipTransform:
    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 
    
    def transform_data(self, data: dict[list[dict[str,any]]], city: str) -> pd.DataFrame: 
        data = data['salaries']
        df = pd.DataFrame(data)

        df['city'] = city 
        df['date_extracted'] = self.date

        return df 
    
    def analytics(self, data: pd.DataFrame, city: str) -> pd.DataFrame: 
        """Expand all of the salary * their occurrence, then calc median"""
        df = pd.DataFrame()

        expanded_df = data.loc[data.index.repeat(data['count'])].reset_index(drop=True)
        df['median_salary'] = np.median(expanded_df['salary'])
        df['city'] = city
        df['date_extracted'] = self.date

        return df
    