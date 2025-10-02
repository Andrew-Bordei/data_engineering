import asyncio 
from zip_extract import ZipExtract
from zip_load import ZipLoad
from zip_transform import ZipTransform
from zip_urls import *

async def zip_pipeline(url: str, city: str, table_name: str):
    """Execute each entity of the pipeline"""
    zip_ext = ZipExtract()
    zip_transform = ZipTransform()
    zip_load = ZipLoad()

    # Extract 
    data = await zip_ext.extract_data(url)
    
    # Transform 
    transformed_df = zip_transform.transform_data(data, city)
    analytics_df = zip_transform.analytics(transformed_df, city)
    
    # Load 
    load_data = zip_load.load_clean_data(transformed_df, table_name)
    load_analytics = zip_load.load_analytics(analytics_df, "zip_analytics")
    return load_data, load_analytics
    
async def zip_async_pipeline():
    """Run all of the functions async for better performance"""

    data = await asyncio.gather(
        zip_pipeline(boise_zip_url, 'boise', 'zip_salaries'),
        zip_pipeline(gr_zip_url, 'grand rapids', 'zip_salaries'),
        zip_pipeline(harrisburg_zip_url, 'harrisburg', 'zip_salaries'),
    )
    return data

if __name__ == "__main__":
    all_data = asyncio.run(zip_async_pipeline())
