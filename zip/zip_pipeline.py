import asyncio 
from zip_extract import ZipExtract
from zip_load import ZipLoad
from zip_transform import ZipTransform
from zip_urls import *

async def zip_pipeline(url: str, city: str, table_name: str):
    zip_ext = ZipExtract()
    zip_transform = ZipTransform()
    zip_load = ZipLoad()

    data = await zip_ext.extract_data(url)
    transformed_df = zip_transform.transform_zip_data(data, city)
    load = zip_load.load_database(transformed_df, table_name)
    return load 

async def zip_async_pipeline():
    data = await asyncio.gather(
        zip_pipeline(boise_zip_url, 'boise', 'zip_salaries'),
        zip_pipeline(gr_zip_url, 'grand rapids', 'zip_salaries'),
        zip_pipeline(harrisburg_zip_url, 'harrisburg', 'zip_salaries'),
    )
    return data

if __name__ == "__main__":
    all_data = asyncio.run(zip_async_pipeline())
