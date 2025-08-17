import requests
import json
import random
from headers import HEADERS

class ZillowSession:
    def __init__(self, headers) -> None:
        # self.payload = payload
        self.user_agent = random.randint(0,10)
        self.headers = headers
        self.headers['User-Agent'] = HEADERS[self.user_agent].get('User-Agent')
        self.session = requests.Session()

    def return_data_safely(self, resp: requests.Session) -> dict:
        if resp.status_code == 200:
            return resp.text
        return None 
    
    def set_payload(self, page: int, west_bound: int, east_bound: int, 
        south_bound: int, north_bound: int, search_term: str, region_id: int):

        payload = json.dumps({
                "searchQueryState": {
                    "pagination": {"currentPage": page},
                    "isMapVisible": False,
                    "mapBounds": {
                        "west": west_bound,
                        "east": east_bound,
                        "south": south_bound,
                        "north": north_bound
                    },
                    "usersSearchTerm": search_term,
                    "regionSelection": [{"regionId": region_id}],
                    "filterState": {"sortSelection": {"value": "globalrelevanceex"}},
                    "isListVisible": True
                },
                "wants": {"cat1": ["listResults"],"cat2": ["total"]},
                "requestId": 2,
                "isDebugRequest": False
            })
        return payload
    
    async def zillow_get_page(self, url: str, headers: dict[str, str], payload: dict) -> dict:
        """Return the house listings for a specific page""" 
        response = await self.session.put(url, headers=headers, data=payload)

        return self.return_data_safely(response)
    