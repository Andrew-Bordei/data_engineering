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
    
    def analytics(self, df: pd.DataFrame, city: str) -> list[any]: 
        """Expand all of the salary * their occurrence, then calc median"""
        data = []

        expanded_df = df.loc[df.index.repeat(df['count'])].reset_index(drop=True)
        median_salary = np.median(expanded_df['salary'])

        data.append(median_salary, city, self.date)
        return data
    