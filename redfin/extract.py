import requests 
import json
import random
import time 
from cookie import COOKIE

class Extract: 
    def __init__(self, region_id: int, state: str, city: str, market: str, region_type: int):
        self.region_id = region_id
        self.state = state
        self.city = city
        self.market = market 
        self.region_type = region_type

    def build_headers(self): 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Referer': f'https://www.redfin.com/city/{self.region_id}/{self.state}/{self.city}',
            'Cookie': COOKIE['Cookie'],
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'TE': 'trailers',
        }
        return headers 

    def build_url(self, page_num: int):
        url = f"https://www.redfin.com/stingray/api/gis?al=1&include_nearby_homes=true&market={self.market}&mpt=99&num_homes=350&ord=days-on-redfin-asc&" \
            f"page_number={page_num}&region_id={self.region_id}&region_type={self.region_type}&sf=1,2,3,5,6,7&start=0&status=9&uipt=1,2,3,4,5,6,7,8&v=8"
        return url 
 
    def request_page(self, url: str, headers: dict[str, str]) -> dict[str, any]:
        response = requests.request("GET", url, headers=headers)
        return response.text
    
    def safely_traverse_dict(self, dict: dict[str: any], *keys) -> any:
        for key in keys:
            try:
                dict = dict[key]
            except KeyError:
                return None
        return dict

    def extract_data(self, data: dict[str, any]): 
        all_houses = []
        data = json.loads(data[4:])
        num_houses = len(data['payload']['homes'])

        for house in range(0, num_houses): 
            base_path = data['payload']['homes'][house]

            mls_num = self.safely_traverse_dict(base_path, 'mlsId', 'value')
            price = self.safely_traverse_dict(base_path, 'price', 'value')
            square_feet = self.safely_traverse_dict(base_path, 'sqFt', 'value')
            lot_size = self.safely_traverse_dict(base_path, 'lotSize', 'value')
            beds = self.safely_traverse_dict(base_path, 'beds')
            baths = self.safely_traverse_dict(base_path, 'baths')
            street_address = self.safely_traverse_dict(base_path, 'streetLine', 'value')
            city = self.safely_traverse_dict(base_path, 'city')
            state = self.safely_traverse_dict(base_path, 'state')
            zip_code = self.safely_traverse_dict(base_path, 'zip')
            time_since_listed = self.safely_traverse_dict(base_path, 'timeOnRedfin', 'value')
            year_built = self.safely_traverse_dict(base_path, 'yearBuilt', 'value')

            house_data = {
                "mls_num": mls_num, 
                "price": price,
                "square_feet": square_feet, 
                "lot_size": lot_size, 
                "beds": beds,  
                "baths": baths, 
                "street_address": street_address, 
                "city": city,
                "state": state, 
                "zip_code": zip_code,
                "time_since_listed": time_since_listed,
                "year_built": year_built,
            }
            all_houses.append(house_data)
        return all_houses
    
    def extraction_process(self, start_page: int, end_page: int): 
        all_data = []

        for page_num in range(start_page, end_page):
            print(f"Getting data on {page_num}")
            url = self.build_url(page_num)
            headers = self.build_headers()
            page = self.request_page(url, headers)
            page_data = self.extract_data(page)
            all_data.extend(page_data)
            time.sleep(random.uniform(0.25, 5))
        return all_data
    