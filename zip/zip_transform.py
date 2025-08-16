import pandas as pd 
from datetime import datetime

class ZipTransform:
    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 
    
    def transform_zip_data(self, data: dict[list[dict[str,any]]], city: str) -> pd.DataFrame: 
        data = data['salaries']
        df = pd.DataFrame(data)

        df['city'] = city 
        df['date_extracted'] = self.date

        return df 