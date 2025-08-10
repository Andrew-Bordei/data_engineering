import json
import time 
import random
import asyncio 
from datetime import datetime
from session import Session
from extract import Extract
from headers import zillow_headers

MAX_PAGES = 21
MIN_SLEEP = 0.5
MAX_SLEEP = 3

class ZillowScraper:
    def __init__(self, url: str, headers: dict[str,str]):
        self.url = url 
        self.headers = headers

    def get_all_data(
        self, west_bound: int, east_bound: int, south_bound: int, 
        north_bound: int, search_term: str, region_id: int 
        ) -> list[dict[str,any]]:

        all_data = []
        sess = Session(headers=self.headers)

        for page in range(1, MAX_PAGES):
            time.sleep(random.uniform(MIN_SLEEP, MAX_SLEEP))
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
                    "regionSelection": [{"regionId": region_id}],
                    "filterState": {
                        "sortSelection": {"value": "globalrelevanceex"}
                    },
                    "isListVisible": True
                },
                "wants": {
                    "cat1": ["listResults"],
                    "cat2": ["total"]
                },
                "requestId": 2,
                "isDebugRequest": False
            })

            data = sess.zillow_get_page(url=url, headers=self.headers, payload=payload)
            all_data.append(data)
        return all_data   
         
    def extracting_data(self, data: list[dict[str,any]]) -> dict[any,any]:
        ext = Extract()
        all_data = []
        num_pages = len(data)

        for i in range(0, num_pages):
            json_data = json.loads(data[i])
            house_data = ext.zillow_extract_data(json_data)
            all_data.append(house_data)
        return all_data
    
    """MAKE THIS ASYNC"""
    def main(self) -> str:
        grand_rapids_data = self.get_all_data(
            west_bound = -85.751532, 
            east_bound = -85.429433, 
            south_bound = 42.852098, 
            north_bound = 43.029051,
            search_term = "Grand Rapids MI homes", 
            region_id = 11671
        )
        grand_rapids = self.extracting_data(grand_rapids_data)

        boise_data = self.get_all_data(
            west_bound = -116.369806, 
            east_bound = -116.043493, 
            south_bound = 43.488708, 
            north_bound = 43.832628,
            search_term = "Boise ID homes", 
            region_id = 3737
        )
        boise = self.extracting_data(boise_data)

        harrisburg_data = self.get_all_data(
            west_bound = -76.932147, 
            east_bound = -76.682837, 
            south_bound = 40.20838, 
            north_bound = 40.434354,
            search_term = "Harrisburg PA homes", 
            region_id = 11817
        )
        harrisburg = self.extracting_data(harrisburg_data)

        return {
            "grand_rapids": grand_rapids, 
            "boise": boise, 
            "harrisburg": harrisburg
        }

if __name__ == '__main__': 
    url = "https://www.zillow.com/async-create-search-page-state"

    zillow_scraper = ZillowScraper(url=url, headers=zillow_headers)

    date = datetime.today().strftime('%Y-%m-%d')

    # data = asyncio.run(zillow_scraper.main())
    data = zillow_scraper.main()

    for city_name, city_data in data.items(): 
        with open(f'zillow_data_{city_name}_{date}.json', 'w', encoding='utf-8') as f:
            json.dump(city_data, f)
