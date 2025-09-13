from extract import Extract
from transform import Transform
from load import Load

# market = 'montana'
# region_id = 2317
# state = 'MT'
# city = 'Bozeman'
# region_type = 6 


def redfin_pipeline(load_method: str, location_params: dict[str, any], 
                    start_page: int, end_page: int): 
    extract = Extract(
        location_params['region_id'],
        location_params['state'], 
        location_params['city'], 
        location_params['market'], 
        location_params['region_type'], 
    )
    transform = Transform()
    load = Load()

    data = extract.extraction_process(start_page, end_page)
    df = transform.transform(data)
    load_df = load.controller(load_method, df)
    
    return load_df

if __name__ == '__main__':
    location_params = {
        "region_id": 2287, 
        "state": 'ID', 
        "city": 'Boise', 
        "market": 'boise',  
        # What type of data are you seraching for? city
        "region_type": 6,
    }
    start_page = 1 
    end_page = 10

    redfin_pipeline('database', location_params, start_page, end_page)