import pandas as pd 
from datetime import datetime

class Transform:
    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d') 

    def convert_time(self, unix: any):
        """Convert time from unix to utc"""
        if pd.isnull(unix) == True:
            return unix
        
        date = datetime.fromtimestamp(unix).strftime('%Y-%m-%d')
        return date

    def clean_data(self, data: list[any]) -> pd.DataFrame: 
        """Clean the dataframe"""

        df = pd.DataFrame(data)

        df['date_price_change'] = df['date_price_change'] / 1000
        df['date_price_change'] = df['date_price_change'].apply(self.convert_time)
        df['date_extracted'] = self.date

        # lower case all string data 
        # strip spaces 

        df = df[[
            'house_id', 'address', 'price', 'tax_assessed_price', 'bedrooms',
            'bathrooms', 'living_sqft', 'lot_sqft', 'lot_unit', 'days_on_zillow',
            'price_change', 'date_price_change', 'zestimate', 'rent_zestimate',
            'home_status', 'home_type', 'non_owner_occupied', 'preforeclosure_auction',
            'premier_builder', 'marketing_status', 'broker', 'country_currency', 
            'date_extracted', 'latitude', 'longitude'
        ]]

        return df 
    
    def data_quality(self, df: pd.DataFrame):
        # Duplicate check (data accuracy) 
        num_duplicates = df['house_id'].duplicated().sum()

        # Null checks (data completeness) 
        house_id_null = df['house_id'].isna().sum()
        address_null = df['address'].isna().sum()
        price_null = df['price'].isna().sum()
        days_listed_null = df['days_on_zillow'].isna().sum()
        latitude_null = df['latitude'].isna().sum()
        longitude_null = df['longitude'].isna().sum()

        data_quality_checks = {
            "num_duplicates": num_duplicates, 
            "house_id_null": house_id_null, 
            "address_null": address_null, 
            "price_null": price_null, 
            "days_listed_null": days_listed_null, 
            "latitude_null": latitude_null,
            "longitude_null": longitude_null 
        }
        return data_quality_checks

    
    def compute_analytics(self, df: pd.DataFrame, city: str) -> list[any]: 
        "Compute dashboard metrics for a city"
        analytics_df = pd.DataFrame()

        # Abstract all of these calcs into their own methods and just call them here 
        num_price_change = df.groupby('date_extracted').agg('count')['price_change']
        num_active_listings = df.groupby('date_extracted')['house_id'].nunique()
        pct_reduced_houses = round((num_price_change / num_active_listings)*100, 2)

        analytics_df['num_active_listings'] = num_active_listings

        analytics_df['pct_reduced_houses'] = pct_reduced_houses

        analytics_df['median_house_price'] = df.groupby('date_extracted').median('price')['price']

        analytics_df['mean_price_reduced'] = round((df.groupby('date_extracted').mean('price_change')['price_change']), 2)

        analytics_df['city'] = city.lower()
        
        analytics_df = analytics_df.reset_index()

        analytics_df = analytics_df[[
            'num_active_listings', 'median_house_price', 'pct_reduced_houses',
            'mean_price_reduced', 'city', 'date_extracted'
        ]]

        return analytics_df 
    