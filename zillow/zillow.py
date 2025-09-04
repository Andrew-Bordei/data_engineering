import asyncio 
from zillow_load import ZillowLoad
from zillow_extract import ZillowExtract
from zillow_transform import ZillowTransform
from headers import zillow_headers
from zillow_constants import *

def zillow_pipeline(
        url: str, headers: dict[str,str], max_pages: int, min_sleep: float, 
        max_sleep: int, west_bound: int, east_bound: int, south_bound: int, 
        north_bound: int, search_term: str, region_id: int, city: str
    ):

    extract = ZillowExtract(url, headers, max_pages, min_sleep, max_sleep)
    transform = ZillowTransform()
    load = ZillowLoad()

    data = extract.extract(
        west_bound, east_bound, south_bound, 
        north_bound, search_term, region_id
    )

    transformed_df = transform.clean_zillow_data(data)
    analytics_df = transform.compute_analytics(transformed_df, city)
    print(analytics_df.head())

    print("Length of data: ", len(transformed_df))

    # load_data = load.load_zillow_data(transformed_df, 'zillow_data') 
    # load_analytics = load.load_analytics(analytics_df, 'zillow_analytics') 

    # return load_data, load_analytics
    return "test"

# async def zillow_async_pipeline():
#     data = await asyncio.gather(
#         zillow_pipeline(
#             zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
#             gr_bounds['west_bound'], gr_bounds['east_bound'], gr_bounds['south_bound'],
#             gr_bounds['north_bound'], gr_bounds['search_term'], gr_bounds['region_id']
#         ),
#         zillow_pipeline(
#             zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
#             boise_bounds['west_bound'], boise_bounds['east_bound'], boise_bounds['south_bound'],
#             boise_bounds['north_bound'], boise_bounds['search_term'], boise_bounds['region_id']
#         ),
#         zillow_pipeline(
#             zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
#             harrisburg_bounds['west_bound'], harrisburg_bounds['east_bound'], harrisburg_bounds['south_bound'],
#             harrisburg_bounds['north_bound'], harrisburg_bounds['search_term'], harrisburg_bounds['region_id']
#         ),
#     )
#     return data

if __name__ == '__main__': 
    grand_rapids_pipeline = zillow_pipeline(
        zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
        gr_bounds['west_bound'], gr_bounds['east_bound'], gr_bounds['south_bound'],
        gr_bounds['north_bound'], gr_bounds['search_term'], gr_bounds['region_id'], 
        "Grand Rapids"
    )

    # boise_pipeline = zillow_pipeline(
    #     zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
    #     boise_bounds['west_bound'], boise_bounds['east_bound'], boise_bounds['south_bound'],
    #     boise_bounds['north_bound'], boise_bounds['search_term'], boise_bounds['region_id'],
    #     "Boise"
    # )

    # harrisburg_pipeline = zillow_pipeline(
    #     zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
    #     harrisburg_bounds['west_bound'], harrisburg_bounds['east_bound'], harrisburg_bounds['south_bound'],
    #     harrisburg_bounds['north_bound'], harrisburg_bounds['search_term'], harrisburg_bounds['region_id'],
    #     "Harrisburg"
    # )

    # all_data = asyncio.run(zillow_async_pipeline())
