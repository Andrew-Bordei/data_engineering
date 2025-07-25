import json
import time 
import random
from datetime import datetime
from session import Session
from extract import Extract

url = "https://www.zillow.com/async-create-search-page-state"

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Referer': 'https://www.zillow.com/homes/?category=SEMANTIC&searchQueryState=%7B%22filterState%22%3A%7B%22isTownhouse%22%3A%7B%22value%22%3Atrue%7D%2C%22isLotLand%22%3A%7B%22value%22%3Atrue%7D%2C%22isManufactured%22%3A%7B%22value%22%3Atrue%7D%2C%22isMultiFamily%22%3A%7B%22value%22%3Atrue%7D%2C%22isApartment%22%3A%7B%22value%22%3Atrue%7D%2C%22isCondo%22%3A%7B%22value%22%3Atrue%7D%2C%22isSingleFamily%22%3A%7B%22value%22%3Atrue%7D%2C%22isApartmentOrCondo%22%3A%7B%22value%22%3Atrue%7D%2C%22isRecentlySold%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketPreForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByAgent%22%3A%7B%22value%22%3Atrue%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Atrue%7D%2C%22isAuction%22%3A%7B%22value%22%3Atrue%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Atrue%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Atrue%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A3737%7D%5D%2C%22usersSearchTerm%22%3A%22Boise%20ID%20homes%22%7D',
  'Content-Type': 'application/json',
  'Origin': 'https://www.zillow.com',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-GPC': '1',
  'Priority': 'u=4'
}

def get_all_data(west_bound, east_bound, south_bound, north_bound,
                search_term, region_id
    ) -> list[dict[str:any]]:
    all_data = []
    sess = Session(headers=headers)

    for page in range(1, 21):
        time.sleep(random.uniform(0.5, 3))
        print(f"Getting the housing data on page: {page}")

        payload = json.dumps({
            "searchQueryState": {
                "pagination": {
                "currentPage": page
                },
                "isMapVisible": False,
                "mapBounds": {
                "west": west_bound,
                "east": east_bound,
                "south": south_bound,
                "north": north_bound
                },
                "usersSearchTerm": search_term,
                "regionSelection": [
                {
                    "regionId": region_id
                }
                ],
                "filterState": {
                "sortSelection": {
                    "value": "globalrelevanceex"
                }
                },
                "isListVisible": True
            },
            "wants": {
                "cat1": [
                "listResults"
                ],
                "cat2": [
                "total"
                ]
            },
            "requestId": 2,
            "isDebugRequest": False
        })

        data = sess.zillow_get_page(url=url, headers=headers, payload=payload)
        all_data.append(data)
    return all_data        

def main(data: list[dict[str:any]]):
    ext = Extract()
    all_data = []
    num_pages = len(data)

    for i in range(0, num_pages):
        json_data = json.loads(data[i])
        house_data = ext.zillow_extract_data(json_data)
        all_data.append(house_data)
    return all_data

if __name__ == '__main__': 
    zillow_data = get_all_data(
        west_bound = -85.751532, 
        east_bound = -85.429433, 
        south_bound = 42.852098, 
        north_bound = 43.029051,
        search_term = "Grand Rapids MI homes", 
        region_id = 11671
    )
    data = main(zillow_data)

    date = datetime.today().strftime('%Y-%m-%d')

    with open(f'zillow_data_grand_rapids_{date}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


    # Boise bounds 
    #  "west": -116.369806,
    #             "east": -116.043493,
    #             "south": 43.488708,
    #             "north": 43.832628
    # boise search term
    # Boise ID homes
    # Boise region id 
    # 3737

    # Grand rapids bounds 
    #  "west": -85.751532,
    #             "east": -85.429433,
    #             "south": 42.852098,
    #             "north": 43.029051
    # grand rapids search term
    # Grand Rapids MI homes
    # grand rapids region id 
    # 11671
    
    # harrisburg bounds 
    #  "west": -76.932147,
    #             "east": -76.682837,
    #             "south": 40.20838,
    #             "north": 40.434354
    # harrisburg search term
    # Harrisburg PA homes
    # harrisburg region id 
    # 11817