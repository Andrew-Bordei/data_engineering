import asyncio 
from zip_extract import ZipExtract
from zip_load import ZipLoad
from zip_urls import *


async def zip_pipeline(url: str, city: str, table_name: str,):
    zip_ext = ZipExtract()
    zip_load = ZipLoad()

    data = await zip_ext.extract_data(url)
    load = zip_load.load_json(data, city)
    return load 

async def get_all_data():
    data = await asyncio.gather(
        zip_pipeline(boise_zip_url, 'boise', 'zip_salaries'),
        zip_pipeline(gr_zip_url, 'grand_rapids', 'zip_salaries'),
        zip_pipeline(harrisburg_zip_url, 'harrisburg', 'zip_salaries'),
    )
    return data

if __name__ == "__main__":
    all_data = asyncio.run(get_all_data())
