import asyncio 
from extract import Extract
from load import Load
from transform import Transform
from urls import *
from log import ScraperLog

async def main(url: str, city: str, table_name: str, logger_name: str):
    """Execute each entity of the pipeline"""
    scraper_log = ScraperLog(logger_name)

    # Instantiate classes for the ETL pipeline  
    extract = Extract()
    transform = Transform()
    load = Load()

    # Extract 
    data = await extract.extract_data(url)
    
    # Transform 
    transformed_df = transform.transform_data(data, city)
    analytics_df = transform.analytics(transformed_df, city)

    # Data quality check 
    data_quality_results = transform.data_quality(transformed_df)

    # Log data quality check
    scraper_log.info(data_quality_results)
    
    # Load 
    load_data = load.load_clean_data(transformed_df, table_name)
    load_analytics = load.load_analytics(analytics_df, "zip_analytics")
    return load_data, load_analytics
    
async def async_main():
    """Run all of the functions async for better performance"""

    data = await asyncio.gather(
        main(boise_zip_url, 'boise', 'zip_salaries', 'boise_logger'),
        main(gr_zip_url, 'grand rapids', 'zip_salaries', 'grand_rapids_logger'),
        main(harrisburg_zip_url, 'harrisburg', 'zip_salaries', 'harrisburg_logger'),
    )
    return data

if __name__ == "__main__":
    all_data = asyncio.run(async_main())
