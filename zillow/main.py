from load import Load
from extract import Extract
from transform import Transform
from headers import zillow_headers
from log import ScraperLog
from constants import *

def pipeline(
        url: str, headers: dict[str,str], max_pages: int, min_sleep: float, 
        max_sleep: int, west_bound: int, east_bound: int, south_bound: int, 
        north_bound: int, search_term: str, region_id: int, logger_name: str
    ):

    scraper_log = ScraperLog(logger_name)

    extract = Extract(url, headers, max_pages, min_sleep, max_sleep)
    transform = Transform()
    load = Load()

    data = extract.extract(
        west_bound, east_bound, south_bound, 
        north_bound, search_term, region_id
    )

    transformed_df = transform.clean_data(data)
    data_quality_results = transform.data_quality(transformed_df)

    # Log data quality check
    scraper_log.info(data_quality_results)

    load_data = load.load_data(transformed_df, 'zillow_data') 
    return load_data

if __name__ == '__main__': 
    grand_rapids_pipeline = pipeline(
        zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
        gr_bounds['west_bound'], gr_bounds['east_bound'], gr_bounds['south_bound'],
        gr_bounds['north_bound'], gr_bounds['search_term'], gr_bounds['region_id'], 
        "zillow_grand_rapids_log"
    )

    boise_pipeline = pipeline(
        zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
        boise_bounds['west_bound'], boise_bounds['east_bound'], boise_bounds['south_bound'],
        boise_bounds['north_bound'], boise_bounds['search_term'], boise_bounds['region_id'],
        "zillow_boise_log"
    )

    harrisburg_pipeline = pipeline(
        zillow_url, zillow_headers, MAX_PAGES, MIN_SLEEP, MAX_SLEEP,
        harrisburg_bounds['west_bound'], harrisburg_bounds['east_bound'], harrisburg_bounds['south_bound'],
        harrisburg_bounds['north_bound'], harrisburg_bounds['search_term'], harrisburg_bounds['region_id'],
        "zillow_harrisburg_log"
    )
