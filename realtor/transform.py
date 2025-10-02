import pandas as pd 
from datetime import datetime

class Transform: 
    def __init__(self)-> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 

    def transform(self, data: dict[str, any]) -> pd.DataFrame:
        df = pd.DataFrame(data)

        df['date_acquired'] = self.date
        return df 